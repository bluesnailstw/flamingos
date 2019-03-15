import Vue from 'vue'
import Router from 'vue-router'

// in development-env not use lazy-loading, because lazy-loading too many pages will cause webpack hot update too slow. so only in production use lazy-loading;
// detail: https://panjiachen.github.io/vue-element-admin-site/#/lazy-loading

Vue.use(Router)

/* Layout */
import Layout from '../views/layout/Layout'

/**
* hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
* alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
*                                if not set alwaysShow, only more than one route under the children
*                                it will becomes nested mode, otherwise not show the root menu
* redirect: noredirect           if `redirect:noredirect` will no redirect in the breadcrumb
* name:'router-name'             the name is used by <keep-alive> (must set!!!)
* meta : {
    title: 'title'               the name show in submenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar,
  }
**/
export const constantRouterMap = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  { path: '/404', component: () => import('@/views/404'), hidden: true },
  {
    path: '',
    component: Layout,
    redirect: 'dashboard',
    name: 'Overview',
    children: [
      {
        path: 'dashboard',
        component: () => import('@/views/dashboard/index'),
        name: 'Dashboard',
        meta: { title: 'dashboard', icon: 'dashboard', noCache: true }
      }
    ]
  }
]

export const asyncRouterMap = [
  {
    path: '/setting',
    component: Layout,
    // alwaysShow: true, // will always show the root menu
    meta: {
      title: '人员管理',
      icon: 'setting',
      roles: ['SU'] // you can set roles in root nav
    },
    children: [
      {
        path: 'users',
        component: () => import('@/views/users/index'),
        name: 'users',
        meta: {
          title: '用户',
          icon: 'user',
          roles: ['SU'] // or you can only set roles in sub nav
        }
      },
      {
        path: 'groups',
        component: () => import('@/views/groups/index'),
        name: 'groups',
        meta: {
          title: '分组',
          icon: 'team',
          roles: ['SU'] // or you can only set roles in sub nav
        }
      }

    ]
  },
  {
    path: '/assets',
    component: Layout,
    meta: {
      title: '资产管理',
      icon: 'cluster',
      roles: ['SU', 'CU'] // you can set roles in root nav
    },
    children: [
      {
        path: 'hosts',
        component: () => import('@/views/hosts/index'),
        name: 'hosts',
        meta: {
          title: '主机',
          icon: 'cloud-server',
          roles: ['SU', 'CU'] // or you can only set roles in sub nav
        }
      },
      {
        path: 'groups',
        component: () => import('@/views/host_groups/index'),
        name: 'groups',
        meta: {
          title: '分组',
          icon: 'cloud-server',
          roles: ['SU', 'CU'] // or you can only set roles in sub nav
        }
        // props: (route) => ({ is_root: route.query.is_root, parent: route.query.parent })
      }
    ]
  },
  {
    path: '/conf',
    component: Layout,
    meta: {
      title: '配置管理',
      icon: 'cluster',
      roles: ['SU', 'CU'] // you can set roles in root nav
    },
    children: [
      {
        path: 'projects',
        component: () => import('@/views/projects/index'),
        name: 'projects',
        meta: {
          title: '项目',
          icon: 'project',
          roles: ['SU', 'CU'] // or you can only set roles in sub nav
        }
      },
      {
        path: 'configurations',
        component: () => import('@/views/configurations/index'),
        name: 'configurations',
        meta: {
          title: '配置',
          icon: 'project',
          roles: ['SU', 'CU'] // or you can only set roles in sub nav
        }
      },
      {
        path: 'inventories',
        component: () => import('@/views/inventories/index'),
        name: 'inventories',
        meta: {
          title: '环境',
          icon: 'project',
          roles: ['SU', 'CU'] // or you can only set roles in sub nav
        }
      }
    ]
  },
  {
    path: '/depoly',
    component: Layout,
    meta: {
      title: '部署管理',
      icon: 'cluster',
      roles: ['SU', 'CU'] // you can set roles in root nav
    },
    children: [
      {
        path: 'tasks',
        component: () => import('@/views/tasks/index'),
        name: 'tasks',
        meta: {
          title: '任务',
          icon: 'project',
          roles: ['SU', 'CU'] // or you can only set roles in sub nav
        }
      },
      {
        path: 'history',
        component: () => import('@/views/history/index'),
        name: 'history',
        meta: {
          title: '历史',
          icon: 'project',
          roles: ['SU', 'CU'] // or you can only set roles in sub nav
        }
      }
    ]
  },

  {
    path: 'gitlab',
    component: Layout,
    children: [
      {
        path: 'http://git.nodevops.cn',
        meta: { title: 'Gitlab', icon: 'link' }
      }
    ]
  },

  { path: '*', redirect: '/404', hidden: true }
]

export default new Router({
  mode: 'history', // 后端支持可开
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})
