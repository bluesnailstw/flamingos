import request from '@/utils/request'

export function fetchList(params) {
  return request({
    url: '/api/tasks/',
    method: 'get',
    params
  })
}
export function fetchOption() {
  return request({
    url: '/api/tasks/',
    method: 'options'
  })
}
export function createItem(data) {
  return request({
    url: '/api/tasks/',
    method: 'post',
    data: data
  })
}
export function updateItem(pk, data) {
  return request({
    url: '/api/tasks/' + pk + '/',
    method: 'patch',
    data: data
  })
}
export function delItem(pk) {
  return request({
    url: '/api/tasks/' + pk + '/',
    method: 'delete'
  })
}
export function deploy(data) {
  return request({
    url: '/deploy',
    method: 'post',
    data: data
  })
}
