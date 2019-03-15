import request from '@/utils/request'

export function fetchList(params) {
  return request({
    url: '/api/users/',
    method: 'get',
    params
  })
}
export function fetchOption() {
  return request({
    url: '/api/users/',
    method: 'options'
  })
}
export function updateItem(pk, data) {
  return request({
    url: '/api/users/' + pk + '/',
    method: 'patch',
    data: data
  })
}
export function delItem(pk) {
  return request({
    url: '/api/users/' + pk + '/',
    method: 'delete'
  })
}
