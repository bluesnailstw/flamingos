<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">新建</el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">导出至Excel</el-button>
    </div>

    <el-table
      v-loading="listLoading"
      :key="tableKey"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange">
      <el-table-column label="ID" prop="id" sortable="custom" align="center" width="65">
        <template slot-scope="scope">
          <span>{{ scope.row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="job" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.job_id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="minion" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.minion_id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <span>test</span>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

  </div>
</template>

<script>
import { fetchList, fetchOption } from '@/api/history'
import waves from '@/directive/waves' // Waves directive
import { toLocaleTime } from '@/utils'
import Pagination from '@/components/Pagination' // Secondary package based on el-pagination

export default {
  name: 'History',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      return ''
    },
    toLocaleTime
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      listOptions: null,
      FileOptions: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        sort: '+id'
      },
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      temp: {
        id: undefined,
        name: '',
        description: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      rules: { },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
    this.getOptions()
  },
  methods: {
    getOptions() {
      fetchOption().then(response => {
        this.listOptions = response
      })
    },
    getList() {
      this.listLoading = true
      fetchList(this.listQuery).then(response => {
        this.list = response.results
        this.total = response.count

        // Just to simulate the time of the request
        this.listLoading = false
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: '操作成功',
        type: 'success'
      })
      row.status = status
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        name: ''
      }
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['ID', '环境名']
        const filterVal = ['id', 'name']
        const data = this.formatJson(filterVal, this.list)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'inventories'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        return v[j]
      }))
    }
  }
}
</script>
