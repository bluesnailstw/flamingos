<template>
  <div class="app-container">
    <div class="filter-container">
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
      <el-table-column label="主机名" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.host_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="内存" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.mem_total }}</span>
        </template>
      </el-table-column>
      <el-table-column label="CPU" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.num_cpus }}</span>
        </template>
      </el-table-column>
      <el-table-column label="使用状态" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.idle_h }}</span>
        </template>
      </el-table-column>
      <el-table-column label="管理状态" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.status_h }}</span>
        </template>
      </el-table-column>
      <el-table-column label="环境" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.inventory_h }}</span>
        </template>
      </el-table-column>
      <el-table-column label="备注" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.comment }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button type="primary" size="mini" @click="handleUpdate(scope.row)">修改</el-button>
          <el-button type="danger" size="mini" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="70px" style="width: 400px; margin-left:50px;">
        <el-form-item label="环境">
          <el-select v-model="temp.inventory" placeholder="请选择">
            <el-option
              v-for="item in inventoryOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"/>
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="temp.status" placeholder="请选择">
            <el-option
              v-for="item in statusOptions"
              :key="item.value"
              :label="item.display_name"
              :value="item.value"/>
          </el-select>
        </el-form-item>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">提交</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import { fetchList, fetchOption, updateItem, delItem } from '@/api/hosts'
import waves from '@/directive/waves' // Waves directive
import { toLocaleTime } from '@/utils'
import Pagination from '@/components/Pagination' // Secondary package based on el-pagination

export default {
  name: 'Hosts',
  components: { Pagination },
  directives: { waves },
  filters: {
    typeFilter(type) {
      return ''
    },
    toLocaleTime
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      listOptions: null,
      inventoryOptions: [],
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
        status: 1,
        inventory: null
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
    this.getOptions()
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      fetchList(this.listQuery).then(response => {
        this.list = response.results
        this.total = response.count

        // Just to simulate the time of the request
        this.listLoading = false
      })
    },
    getOptions() {
      fetchOption().then(response => {
        this.listOptions = response
        this.statusOptions = this.listOptions.actions.POST.status.choices
        this.inventoryOptions = this.listOptions.ext.inventories
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
        id: undefined
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          return
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = {
            name: this.temp.name,
            inventory: this.temp.inventory
          }
          updateItem(this.temp.id, tempData).then(() => {
            for (const v of this.list) {
              if (v.id === this.temp.id) {
                const index = this.list.indexOf(v)
                this.list.splice(index, 1, this.temp)
                break
              }
            }
            this.dialogFormVisible = false
            this.$notify({
              title: '成功',
              message: '更新成功',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleDelete(row) {
      const pk = row.id
      this.$confirm('此操作将永久删除该内容, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delItem(pk).then(res => {
          this.$notify({
            title: '成功',
            message: '删除成功',
            type: 'success',
            duration: 2000
          })
          const index = this.list.indexOf(row)
          this.list.splice(index, 1)
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['ID', '主机名']
        const filterVal = ['id', 'host_name']
        const data = this.formatJson(filterVal, this.list)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'groups'
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
