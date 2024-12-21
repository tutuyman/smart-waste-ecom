<template>
  <el-table
    :data="paginatedData"
    style="width: 100%; overflow-x: auto;"
    fit="true"
  >

    <!-- Iterasi headers menggunakan v-for untuk membuat kolom dinamis -->
    <el-table-column
      v-for="header in headers"
      :key="header.prop"
      :prop="header.prop"
      :label="header.label"
      :sortable="header.prop !== 'action'"
      :min-Width="isProductTable === false && header.prop === 'action' ? '150' : header.minWidth"
    >
      <!-- Template khusus untuk Discount agar tampil sebagai persentase -->
      <template v-if="header.prop === 'discFromRetail'" #default="{ row }">
        <span>{{ (row.discFromRetail * 100).toFixed() }}%</span>
      </template>

      <template v-else-if="header.prop === 'action' && isProductTable == true" #default="{ row }">
        <button class="button-submit" @click="buttonModal(row)">
          Submit
        </button>
      </template>

      <template v-else-if="header.prop === 'action' && isProductTable == false" #default="{ row }">
        <div>
          <el-button class="button-action" type="success" @click="handleSuccess(row)">
            <el-icon><Check/></el-icon>
          </el-button>
          <el-button  class="button-action" type="danger" :icon="Edit" @click="handleReject(row)">
            <el-icon><Close /></el-icon>
          </el-button>
        </div>
      </template>

      <!-- Default template untuk kolom lainnya -->
      <template v-else #default="{ row }">
        <span>{{ row[header.prop] }}</span>
      </template>
    </el-table-column>
  </el-table>

  <el-pagination
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"
    :current-page="currentPage"
    :page-sizes="[10, 20, 30, 50]"
    :page-size="pageSize"
    layout="prev, pager, next, total, sizes"
    :total="total"
    style="margin-top: 20px;"
  />
</template>

<script>
import { ref, defineComponent } from 'vue';
import { ElTable, ElTableColumn, ElPagination, ElAvatar } from 'element-plus';
import { Check, EditPen, Close } from '@element-plus/icons-vue';
import { acceptBid, rejectBid } from "../api/bids.js"

export default defineComponent({
  components: {
    ElTable,
    ElTableColumn,
    ElPagination,
    ElAvatar,
    Check,
    EditPen,
    Close,
  },
  props: {
    tableData: {
      type: Array,
      required: true,
    },
    headers: {
      type: Array,
      required: true,
    },
    buttonModal: {
      type: Function,
      required: true,
    },
    isProductTable: {
      type: Boolean,
      required: false,
    }
  },
  setup() {
    const currentPage = ref(1);
    const pageSize = ref(10);

    const handleSizeChange = (val) => {
      pageSize.value = val;
    };

    const handleCurrentChange = (val) => {
      currentPage.value = val;
    };

    return {
      currentPage,
      pageSize,
      handleSizeChange,
      handleCurrentChange,
    };
  },
  computed: {
    // Total number of records
    total() {
      return this.tableData.length;
    },
    // Data to display on the current page
    paginatedData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = this.currentPage * this.pageSize;
      return this.tableData.slice(start, end);
    },
  },
  methods: {
    handleSuccess(row) {
      console.log('Success');
      acceptBid(row.id);
      row.status = "ACCEPTED";
    },
    handleEdit() {
      console.log('Edit');
    },
    handleReject(row) {
      console.log('Reject');
      rejectBid(row.id);
      row.status = "REJECTED";
    }
  },
});
</script>

<style scoped>
.el-table__header {
  background-color: black !important;
}

.button-submit {
  color: #FFFFFF;
  background-color: #111827;

  width: 99px;
  height: 100%;
  border-radius: 10px;
  cursor: pointer;
}

.button-action{
  width: 30px;
  color: #FFFFFF;
}
</style>
