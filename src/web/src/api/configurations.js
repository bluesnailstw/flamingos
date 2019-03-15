import request from '@/utils/request'

export function fetchList(params) {
  return request({
    url: '/api/configurations/',
    method: 'get',
    params
  })
}
export function fetchOption() {
  return request({
    url: '/api/configurations/',
    method: 'options'
  })
}
export function createItem(data) {
  return request({
    url: '/api/configurations/',
    method: 'post',
    data: data
  })
}
export function updateItem(pk, data) {
  return request({
    url: '/api/configurations/' + pk + '/',
    method: 'patch',
    data: data
  })
}
export function delItem(pk) {
  return request({
    url: '/api/configurations/' + pk + '/',
    method: 'delete'
  })
}
