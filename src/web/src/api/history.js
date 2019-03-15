import request from '@/utils/request'

export function fetchList(params) {
  return request({
    url: '/api/history/',
    method: 'get',
    params
  })
}
export function fetchOption() {
  return request({
    url: '/api/history/',
    method: 'options'
  })
}
