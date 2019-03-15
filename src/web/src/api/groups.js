import request from '@/utils/request'

export function fetchList(params) {
  return request({
    url: '/api/user_groups/',
    method: 'get',
    params
  })
}
export function fetchOption() {
  return request({
    url: '/api/user_groups/',
    method: 'options'
  })
}
export function createItem(data) {
  return request({
    url: '/api/user_groups/',
    method: 'post',
    data: data
  })
}
export function updateItem(pk, data) {
  return request({
    url: '/api/user_groups/' + pk + '/',
    method: 'patch',
    data: data
  })
}
export function delItem(pk) {
  return request({
    url: '/api/user_groups/' + pk + '/',
    method: 'delete'
  })
}
