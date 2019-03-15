<template>
  <div class="dashboard-container">
    <component :is="currentRole"/>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import SUDashboard from './SU'
import CUDashboard from './CU'

export default {
  name: 'Dashboard',
  components: { SUDashboard, CUDashboard },
  data() {
    return {
      currentRole: 'SUDashboard'
    }
  },
  computed: {
    ...mapGetters([
      'roles'
    ])
  },
  created() {
    if (!this.roles.includes('SU')) {
      this.currentRole = 'CUDashboard'
    }
  }
}
</script>
