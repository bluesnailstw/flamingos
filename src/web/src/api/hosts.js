import request from '@/utils/request'

export function fetchList(params) {
  return request({
    url: '/api/hosts/',
    method: 'get',
    params
  })
}
export function fetchOption() {
  return request({
    url: '/api/hosts/',
    method: 'options'
  })
}
export function updateItem(pk, data) {
  return request({
    url: '/api/hosts/' + pk + '/',
    method: 'patch',
    data: data
  })
}
export function delItem(pk) {
  return request({
    url: '/api/hosts/' + pk + '/',
    method: 'delete'
  })
}
