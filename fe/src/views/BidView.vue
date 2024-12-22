<script>
import { CgMathPlus, ClFileDownload } from '@kalimahapps/vue-icons';
import datatabledummy from '../utils/DataTableDummy.js';
import TableComponent from '@/components/TableComponent.vue';
import { Search, ArrowDown } from '@element-plus/icons-vue';
import BidTableColumn from '../utils/BidTableColumn.js';
import {getBids} from '../api/bids';

export default {
  components: {
    CgMathPlus,
    ClFileDownload,
    TableComponent,
    Search,
    ArrowDown,
  },
  data() {
    return {
      datatabledummy,
      datatable: [],
      input1: '', // Tambahkan data ini untuk v-model di el-input
      BidTableColumn,
    };
  },
  async created() {
    if (localStorage.getItem("role") != "ADMIN" ){
      this.BidTableColumn = BidTableColumn.filter(col => col.prop != "action");
    }

    const bids = await getBids();

    this.datatable = bids.map(b => (
      {
        "userId": b.user_id,
        "id": b.id,
        "product": b.product.name,
        "productId": b.product.id,
        "quantity": b.quantity,
        "bidPrice": b.offer_price,
        "expireDate": b.product.expiry_date,
        "productCost": b.product.product_cost,
        "retailPrice": b.product.retail_price,
        "discFromRetail": b.product.discount,
        "offerPrice": b.product.offer_price,
        "status": b.status,
      }
    ))
  }
};
</script>

<template>
  <div class="content">
    <div class="content-header">
      <div class="content-header-left">
        <h1>Bid</h1>
        <p>Manage your bid list</p>
      </div>
      <div class="content-header-right">
        <button class="right-button profile-button">
          <ClFileDownload class="icon-button" />
          Download
        </button>
      </div>
    </div>
    <div class="content-table">
      <div class="content-filter">
        <div class="content-filter-left">
          <el-input
            v-model="input1"
            placeholder="Search products"
            size="large"
            style="width: 560px;"
            :suffix-icon="Search"
          />
          <el-dropdown class="dropdown">
            <span class="el-dropdown-link">
              All Category
              <el-icon class="el-icon--right">
                <arrow-down />
              </el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu class="custom-dropdown-menu">
                <el-dropdown-item>Category 1</el-dropdown-item>
                <el-dropdown-item>Category 2</el-dropdown-item>
                <el-dropdown-item>Category 3</el-dropdown-item>
                <el-dropdown-item>Category 4</el-dropdown-item>
                <el-dropdown-item>Category 5</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
        <div class="content-filter-right">
        </div>
      </div>
      <TableComponent :tableData="datatable" :headers="BidTableColumn" />
    </div>
  </div>
</template>

<style scoped>
h1 {
  font-size: 24px;
  font-weight: 400;
  margin: 0;
}

.table {
  background-color: #FFFFFF;
  padding: 10px;
}

.content-header {
  display: flex;
  justify-content: space-between;
}
.content-filter {
  padding: 10px;
  display: flex;
  justify-content: space-between;
}
.content-header-left p {
  margin: 10px 0;
  color: #687588;
}

.p-datatable thead tr {
  background-color: #f9f9f9;
}

.p-datatable tbody tr td,
.p-datatable thead tr th {
  border: none;
  padding: 10px; /* atau padding sesuai kebutuhan */
}

.content-header-right {
  display: flex;
  gap: 20px;
}

.button-filter {
  color: #FFFFFF;
  background-color: #111827;

  width: 99px;
  height: 100%;
  border-radius: 10px;
}

.dropdown {
  border: 1px solid #eaeaea;
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 160px;
  height: 48px;
}

.content-table {
  background-color: #FFFFFF;
  padding: 10px;
  border-radius: 16px;
  margin-top: 20px;
}

.dropdown .el-dropdown-link:focus,
.dropdown .el-icon--right:focus {
  outline: none; /* Menyembunyikan outline */
}

.custom-dropdown-menu {
  width: 156px; /* Sesuaikan lebar yang diinginkan */
}

.right-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: 1px solid #111827;
  border-radius: 10px;
  width: 150px;
  height: 56px;
  font-size: 16px;
  font-weight: 700;
  color: #111827;
}

.content-filter-left {
  display: flex;
  gap: 16px
}

.icon-button {
  font-size: 20px;
  color: #111827;
  font-weight: 500;
}

.el-dropdown-link {
  cursor: pointer;
  display: flex;
  font-size: 16px;
  align-items: center;
}
</style>
