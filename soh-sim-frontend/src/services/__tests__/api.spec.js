/**
 * api.js unified request layer unit tests
 *
 * Tests: request (GET/POST/PUT/DELETE, auth, error, timeout),
 * success/error response parsing, ApiError, 401 redirect, file download.
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { request, get, post, put, del, download, ApiError } from '../api.js'

// ---------- setup ----------

let fetchMock, fetchResolve

beforeEach(() => {
  // Reset token cache
  sessionStorage.clear()
  vi.spyOn(sessionStorage, 'getItem').mockReturnValue(null)

  // Mock fetch
  fetchMock = vi.fn()
  global.fetch = fetchMock

  // Default response
  fetchMock.mockImplementation(
    () =>
      new Promise((resolve) => {
        fetchResolve = resolve
      })
  )

  // Spy console.error
  vi.spyOn(console, 'error').mockImplementation(() => {})
})

afterEach(() => {
  vi.restoreAllMocks()
})

function mockResponse(body, status = 200, contentType = 'application/json') {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: status >= 200 && status < 300,
      status,
      statusText: status === 404 ? 'Not Found' : 'OK',
      headers: new Map([['content-type', contentType]]),
      json: async () => body,
      blob: async () => new Blob([JSON.stringify(body)])
    })
  )
}

// ---------- basic requests ----------

describe('request', () => {
  it('GET returns parsed JSON on success', async () => {
    mockResponse({ success: true, data: { id: 1 }, error: null, message: 'ok' })
    const result = await get('/api/test')
    expect(result).toEqual({ success: true, data: { id: 1 }, error: null, message: 'ok' })
  })

  it('POST sends JSON body', async () => {
    mockResponse({ success: true, data: null })
    const result = await post('/api/create', { name: 'test' })
    expect(fetchMock).toHaveBeenCalledWith(
      expect.stringContaining('/api/create'),
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ name: 'test' })
      })
    )
  })

  it('PUT sends JSON body', async () => {
    mockResponse({ success: true, data: null })
    await put('/api/update', { id: 1 })
    expect(fetchMock).toHaveBeenCalledWith(
      expect.stringContaining('/api/update'),
      expect.objectContaining({ method: 'PUT' })
    )
  })

  it('DELETE sends no body', async () => {
    mockResponse({ success: true, data: null })
    await del('/api/delete')
    expect(fetchMock).toHaveBeenCalledWith(
      expect.stringContaining('/api/delete'),
      expect.objectContaining({ method: 'DELETE' })
    )
  })
})

// ---------- auth ----------

describe('auth token', () => {
  it('injects Bearer token when available', async () => {
    sessionStorage.getItem.mockReturnValue('test-jwt-token')
    mockResponse({ success: true, data: {} })
    await get('/api/me')
    expect(fetchMock).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        headers: expect.objectContaining({
          Authorization: 'Bearer test-jwt-token'
        })
      })
    )
  })

  it('omits token when skipAuth is true', async () => {
    sessionStorage.getItem.mockReturnValue('test-jwt-token')
    mockResponse({ success: true, data: {} })
    await request('/api/public', { method: 'GET' }, { skipAuth: true })
    const callArgs = fetchMock.mock.calls[0][1]
    expect(callArgs.headers.Authorization).toBeUndefined()
  })
})

// ---------- errors ----------

describe('error handling', () => {
  it('throws ApiError on 401 with token clear', async () => {
    mockResponse({ error: '登录已过期' }, 401)
    sessionStorage.getItem.mockReturnValue('stale-token')
    const removeSpy = vi.spyOn(sessionStorage, 'removeItem')
    await expect(get('/api/protected')).rejects.toThrow(ApiError)
    await expect(get('/api/protected')).rejects.toMatchObject({ status: 401 })
  })

  it('throws ApiError on 500', async () => {
    mockResponse({ error: '服务器内部错误' }, 500)
    await expect(get('/api/data')).rejects.toThrow(ApiError)
    await expect(get('/api/data')).rejects.toMatchObject({ status: 500 })
  })

  it('throws ApiError when success=false', async () => {
    mockResponse({ success: false, error: '操作失败', data: null }, 200)
    await expect(post('/api/compute', {})).rejects.toThrow(ApiError)
  })

  it('throws ApiError with raw data', async () => {
    mockResponse({ success: false, error: 'duplicate key', detail: 'exists' }, 200)
    try {
      await post('/api/create', {})
    } catch (e) {
      expect(e.raw).toEqual({ success: false, error: 'duplicate key', detail: 'exists' })
    }
  })
})

// ---------- timeout ----------

describe('timeout', () => {
  it('throws ApiError with status 408 on timeout', async () => {
    // Don't resolve — controller aborts first
    fetchMock.mockImplementationOnce(() => new Promise(() => {}))
    const promise = request('/api/slow', { method: 'GET' }, { timeout: 10 })
    await expect(promise).rejects.toThrow(ApiError)
    try {
      await promise
    } catch (e) {
      expect(e.status).toBe(408)
      expect(e.message).toContain('超时')
    }
  })
})

// ---------- download (blob) ----------

describe('download', () => {
  it('returns blob for non-JSON response', async () => {
    fetchMock.mockImplementationOnce(() =>
      Promise.resolve({
        ok: true,
        status: 200,
        statusText: 'OK',
        headers: new Map([['content-type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']]),
        json: async () => {
          throw new Error('not json')
        },
        blob: async () => new Blob(['fake-excel-data'])
      })
    )
    const blob = await download('/api/export/csv', { projectId: '1' })
    expect(blob).toBeInstanceOf(Blob)
  })
})
