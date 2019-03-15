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
      <el-table-column label="描述" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.description }}</span>
        </template>
      </el-table-column>
      <el-table-column label="状态" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.status }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button type="waning" size="mini" @click="openDialogDeploy(scope.row)">部署</el-button>
          <el-button type="primary" size="mini" @click="handleUpdate(scope.row)">修改</el-button>
          <el-button type="danger" size="mini" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogFormStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="70px" style="width: 400px; margin-left:50px;">
        <el-form-item label="项目">
          <el-select v-model="temp.project" placeholder="请选择">
            <el-option
              v-for="item in ProjectOptions"
              :key="item.value"
              :label="item.display_name"
              :value="item.value"/>
          </el-select>
        </el-form-item>
        <el-form-item label="发布日志">
          <el-input v-model="temp.description" type="text"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="dialogFormStatus==='create'?createData():updateData()">提交</el-button>
      </div>
    </el-dialog>

    <el-dialog
      :visible.sync="dialogDeployVisible"
      title="部署"
      width="80%"
      @open="HandleDialogDeployOpen()"
      @close="HandleDialogDeployClose()">

      <el-row type="flex" class="row-bg" style="margin-top: 10px;">
        <el-col>
          <span style="margin-right: 5px">目标</span>
          <el-select v-model="target" clearable placeholder="请选择" @change="handleFilter">
            <el-option
              v-for="item in targetOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"/>
          </el-select>
        </el-col>
        <el-col>
          <el-popover
            v-model="dialogDeployConfirmVisible"
            placement="top"
            width="160">
            <p>确定要发布这个任务吗？</p>
            <div style="text-align: right; margin: 0">
              <el-button size="mini" type="text" @click="dialogDeployConfirmVisible = false">取消</el-button>
              <el-button type="primary" size="mini" @click="handleDeploy()">确定</el-button>
            </div>
            <el-button slot="reference" type="primary">确 定</el-button>
          </el-popover>
        </el-col>
      </el-row>
      <el-row type="flex" class="row-bg" style="margin-top: 10px;">
        <el-col>
          <el-table
            :data="deployLogs"
            :row-class-name="deployResult"
            style="width: 100%">
            <el-table-column type="expand">
              <template slot-scope="props">
                <el-form label-position="left" inline>
                  <el-form-item
                    v-for="(value, key, index) in props.row.return"
                    :key="index"
                    :label="key">
                    <span>{{ value }}</span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <el-table-column
              label="主机 ID">
              <template slot-scope="props">
                <span>{{ props.row.id }} </span>
              </template>
            </el-table-column>
            <el-table-column
              label="返回码">
              <template slot-scope="props">
                <span>{{ props.row.retcode }} </span>
              </template>
            </el-table-column>
            <el-table-column
              label="成功">
              <template slot-scope="props">
                <span>{{ props.row.success }} </span>
              </template>
            </el-table-column>
            <el-table-column align="right">
              <template slot="header" slot-scope="scope">
                <el-input
                  v-model="env"
                  size="mini"
                  placeholder="输入关键字搜索"/>
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogDeployVisible = false">取 消</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<style>
  .el-table .warning-row {
    background: orangered;
  }
  .el-table .error-row {
    background: firebrick;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
</style>

<script>
import { fetchList, createItem, updateItem, fetchOption, delItem, deploy } from '@/api/tasks'
import waves from '@/directive/waves' // Waves directive
import { toLocaleTime } from '@/utils'
import Pagination from '@/components/Pagination' // Secondary package based on el-pagination

export default {
  name: 'Tasks',
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
      HostsOptions: null,
      ProjectOptions: null,
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
        hosts: [],
        project: '',
        description: ''
      },
      dialogFormVisible: false,
      dialogDeployVisible: false,
      dialogDeployConfirmVisible: false,
      dialogFormStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      rules: { },
      downloadLoading: false,
      task: null,
      ws: null,
      deployLogs: [],
      env: null
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
    deployResult({ row, rowIndex }) {
      // console.info(row)
      // if (row.retcode === 0) {
      //   return 'success-row'
      // } else {
      //   return 'error-row'
      // }
    },
    displayDeployLog(msg) {
      console.info(msg)
      const data = JSON.parse(msg.data)
      this.deployLogs.push(data)
    },
    HandleDialogDeployOpen() {
      this.ws = new WebSocket('ws://centos:8080/ws')

      this.ws.onmessage = this.displayDeployLog
    },
    HandleDialogDeployClose() {
      this.ws.close()
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
    handleCreate() {
      this.resetTemp()
      this.dialogFormStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = {
            hosts: this.temp.hosts,
            project: this.temp.project,
            description: this.temp.description
          }
          createItem(tempData).then(() => {
            this.list.unshift(this.temp)
            this.dialogFormVisible = false
            this.$notify({
              title: '成功',
              message: '创建成功',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.dialogFormStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    handleDeploy() {
      this.dialogDeployConfirmVisible = false
      deploy({ task_id: this.task.id }).then(res => {
        this.ws.send(JSON.stringify({ action: 'add_job', job: res.data }))
        this.$notify({
          title: '成功',
          message: '启动成功',
          type: 'success',
          duration: 2000
        })
      })
    },
    openDialogDeploy(row) {
      this.dialogDeployVisible = true
      this.task = Object.assign({}, row) // copy obj
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = {
            hosts: this.temp.hosts,
            project: this.temp.project,
            description: this.temp.description
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
        const tHeader = ['ID', '发布日志']
        const filterVal = ['id', 'description']
        const data = this.formatJson(filterVal, this.list)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'tasks'
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
