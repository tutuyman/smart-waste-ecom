<script>
import { Search, ArrowDown } from '@element-plus/icons-vue';
import { CgMathPlus, ClFileDownload } from "@kalimahapps/vue-icons";
import datatabledummy from "../utils/DataTableDummy.js";
import TableComponent from "@/components/TableComponent.vue";
import ProductTableColumn from "../utils/ProductTableColumn.js";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";
import Button from "primevue/button";

import {getProductOffers} from "../api/products"
import {postBid} from "../api/bids";

export default {
  components: {
    CgMathPlus,
    ClFileDownload,
    TableComponent,
    Dialog,
    InputText,
    Button,
    Search,
    ArrowDown,
  },
  data() {
    return {
      datatable: [],
      ProductTableColumn,
      dialogVisible: false, // Properti reaktif untuk mengontrol modal
      dataDialog: null,
      quantity: 0,
      offerPrices: 0,
      searchValue: '',
    };
  },
  async created() {
    if (localStorage.getItem("role") == "ADMIN" ){
      this.ProductTableColumn = ProductTableColumn.filter(col => col.prop != "action");
    } else {
      this.ProductTableColumn = ProductTableColumn.filter(col => col.prop != "userId");
    }

    let productOffers = await getProductOffers();

    let datatable = [];

    for(const prod of productOffers) {
      for (const offer of prod.product_offers) {
        datatable.push({
          userId: offer.user_id,
          id: Math.floor(Math.random() * 1000) || 0,
          product: prod.name || "",
          productId: prod.id || "",
          stock: prod.stock || 0,
          expireDate: prod.expiry_date || "",
          retailPrice: prod.retail_price || 0,
          discFromRetail: (offer.discount || 0.0),
          offerPrice: offer.offer_price || 0.0,
        }
      )
      }
    }

    this.datatable = datatable;
  },
  methods: {
    openDialog(data) {
      this.quantity = 0;
      this.dataDialog = data; // Langsung tetapkan data
      this.dialogVisible = !!this.dataDialog; // Dialog hanya muncul jika data ada
    },
    closeDialog() {
      postBid({
        product_id: this.dataDialog.productId,
        offer_price: this.offerPrices,
        quantity: this.quantity,
      })
      this.dialogVisible = false;
    },
    validatePrices(value) {
      // Hapus semua karakter non-angka
      const numericValue = value.replace(/[^0-9]/g, ''); // Izinkan hanya angka
      this.offerPrices = numericValue === '' ? '' : String(Math.max(0, parseInt(numericValue, 10)));
    },
    validateQuantity(value) {
      // Hapus semua karakter non-angka
      const numericValue = value.replace(/[^0-9]/g, ''); // Izinkan hanya angka
      const parsedValue = numericValue === '' ? 0 : Math.max(0, parseInt(numericValue, 10));

      // Validasi agar tidak lebih besar dari dataDialog.stock
      if (parsedValue > this.dataDialog.stock) {
        this.quantity = String(this.dataDialog.stock); // Set ke stok maksimum jika melebihi
      } else {
        this.quantity = String(parsedValue);
      }
    }
  },
};
</script>

<template>
  <div class="content">
    <!-- Header -->
    <div class="content-header">
      <div class="content-header-left">
        <h1>Product</h1>
        <p>Manage your order</p>
      </div>
      <div class="content-header-right">
        <button class="right-button">
          <CgMathPlus class="icon-button" />
          Upload
        </button>
      </div>
    </div>

    <!-- Table -->
    <div class="content-table">
      <div class="content-filter">
        <div class="content-filter-left">
          <el-input
            v-model="searchValue"
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
      <TableComponent 
        :tableData="datatable" 
        :headers="ProductTableColumn" 
        :buttonModal="openDialog" 
        :isProductTable="true"
      />
    </div>

    <!-- Dialog -->
    <el-dialog
      v-model="dialogVisible"
      title="Tips"
      width="600"
      :before-close="handleClose"
    >
      <div class="dialog-content">
        <div class="dialog-left-content">
          <div class="dialog-left-content">
            <div class="field">
              <span class="label">Product Name:</span><span class="value">{{ dataDialog?.product }}</span>
            </div>
            <div class="field">
              <span class="label">Stock:</span><span class="value">{{ dataDialog?.stock }}</span>
            </div>
            <div class="field">
              <span class="label">Retail Price:</span><span class="value">{{ dataDialog?.retailPrice }}</span>
            </div>
          </div>
        </div>
        <div class="dialog-right-content">
          <div class="field">
            <span class="label">Discount:</span><span class="value">{{ (dataDialog?.discFromRetail*100).toFixed() }}%</span>
          </div>
          <div class="field">
            <span class="label">Offer Prices:</span>
            <el-input
              v-model="offerPrices"
              type="text"
              placeholder="Input Prices"
              class="custom-number-input"
              @input="validatePrices"
            >
            </el-input>
          </div>
          <div class="field">
            <span class="label">Quantity:</span>
            <el-input
              v-model="quantity"
              type="text"
              placeholder="Input Quantity"
              class="custom-number-input"
              @input="validateQuantity"
            >
            </el-input>
          </div>
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="closeDialog">Cancel</el-button>
          <el-button type="primary" @click="closeDialog">
            Confirm
          </el-button>
        </div>
      </template>
    </el-dialog>
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

.el-input-number__increase,
.el-input-number__decrease {
  display: none;
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

.dialog-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start; /* Sesuaikan jika perlu vertikal alignment */
  width: 100%; /* Pastikan parent element memiliki lebar yang diinginkan */
  padding-bottom: 18px;
  font-size: 16px;
  font-weight: 500;
}

.dialog-left-content,
.dialog-right-content {
  display: flex;
  flex-direction: column; /* Kolom untuk setiap pasangan label dan value */
  gap: 10px; /* Jarak antar pasangan label dan value */
}

.field {
  display: flex;
  justify-content: space-between; /* Label dan value berjauhan dalam satu baris */
  align-items: center; /* Memastikan label dan value sejajar secara vertikal */
}

.label {
  font-weight: bold; /* Opsional: memberikan gaya tebal untuk label */
  margin-right: 10px; /* Jarak antara label dan value */
  flex-shrink: 0; /* Memastikan label tidak menyusut */
}

.value {
  flex-grow: 1; /* Membiarkan value memenuhi sisa ruang */
  text-align: right; /* Opsional: rata kanan untuk value */
}

.dialog-left-content span,
.dialog-right-content span {
  display: flex; /* Pastikan elemen dalam kolom berada dalam baris terpisah */
  margin-bottom: 5px; /* Opsional, tambahkan jarak antar teks */
}

</style>
