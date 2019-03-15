import request from '@/utils/request'

export function login(username, password) {
  const bodyFormData = new FormData()
  bodyFormData.set('username', username)
  bodyFormData.set('password', password)
  return request({
    url: 'login',
    method: 'post',
    data: bodyFormData,
    config: { headers: { 'Content-Type': 'multipart/form-data' }}
  })
}

export function getInfo(token) {
  return request({
    url: '/user',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: 'logout',
    method: 'get'
  })
}
