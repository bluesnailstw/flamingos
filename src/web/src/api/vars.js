import request from '@/utils/request'

export function fetchList(params) {
  return request({
    url: '/api/vars/',
    method: 'get',
    params
  })
}
export function fetchOption() {
  return request({
    url: '/api/vars/',
    method: 'options'
  })
}
export function updateItem(pk, data) {
  return request({
    url: '/api/vars/' + pk + '/',
    method: 'patch',
    data: data
  })
}
export function delItem(pk) {
  return request({
    url: '/api/vars/' + pk + '/',
    method: 'delete'
  })
}
