import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

// Types
export interface Vendor {
  id: number;
  vendorCode: string;
  name: string;
  contactPerson: string;
  email: string;
  phone: string;
  address: string;
  taxId: string;
  paymentTerms: string;
  creditLimit: number;
  status: 'Active' | 'Inactive';
  category: string;
  rating: number;
}

export interface APInvoice {
  id: number;
  invoiceNumber: string;
  vendorId: number;
  vendorName: string;
  invoiceDate: string;
  dueDate: string;
  amount: number;
  taxAmount: number;
  totalAmount: number;
  status: 'draft' | 'approved' | 'paid' | 'overdue' | 'cancelled';
  description: string;
  reference: string;
  createdBy: string;
  createdAt: string;
  approvedBy?: string;
  approvedAt?: string;
  paidAt?: string;
  lines: APInvoiceLine[];
}

export interface APInvoiceLine {
  id: number;
  description: string;
  quantity: number;
  unitPrice: number;
  amount: number;
  taxRate: number;
  taxAmount: number;
  totalAmount: number;
}

export interface Payment {
  id: number;
  paymentNumber: string;
  vendorId: number;
  vendorName: string;
  paymentDate: string;
  amount: number;
  paymentMethod: string;
  reference: string;
  status: 'pending' | 'completed' | 'failed' | 'cancelled';
  description: string;
  createdBy: string;
  createdAt: string;
  completedAt?: string;
  invoiceIds: number[];
}

export interface PurchaseOrder {
  id: number;
  poNumber: string;
  vendorId: number;
  vendorName: string;
  orderDate: string;
  expectedDeliveryDate: string;
  totalAmount: number;
  status: 'draft' | 'sent' | 'confirmed' | 'received' | 'cancelled';
  description: string;
  createdBy: string;
  createdAt: string;
  lines: PurchaseOrderLine[];
}

export interface PurchaseOrderLine {
  id: number;
  description: string;
  quantity: number;
  unitPrice: number;
  amount: number;
  receivedQuantity: number;
}

export interface AccountsPayableState {
  vendors: Vendor[];
  invoices: APInvoice[];
  payments: Payment[];
  purchaseOrders: PurchaseOrder[];
  loading: boolean;
  error: string | null;
  selectedVendor: Vendor | null;
  selectedInvoice: APInvoice | null;
  selectedPayment: Payment | null;
  selectedPO: PurchaseOrder | null;
}

const initialState: AccountsPayableState = {
  vendors: [],
  invoices: [],
  payments: [],
  purchaseOrders: [],
  loading: false,
  error: null,
  selectedVendor: null,
  selectedInvoice: null,
  selectedPayment: null,
  selectedPO: null,
};

// Async thunks
export const fetchVendors = createAsyncThunk(
  'accountsPayable/fetchVendors',
  async (_, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      return [];
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchInvoices = createAsyncThunk(
  'accountsPayable/fetchInvoices',
  async (_, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      return [];
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchPayments = createAsyncThunk(
  'accountsPayable/fetchPayments',
  async (_, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      return [];
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchPurchaseOrders = createAsyncThunk(
  'accountsPayable/fetchPurchaseOrders',
  async (_, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      return [];
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

export const createVendor = createAsyncThunk(
  'accountsPayable/createVendor',
  async (vendor: Omit<Vendor, 'id'>, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 500));
      return { ...vendor, id: Date.now() };
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

export const createInvoice = createAsyncThunk(
  'accountsPayable/createInvoice',
  async (invoice: Omit<APInvoice, 'id'>, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 500));
      return { ...invoice, id: Date.now() };
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

export const createPayment = createAsyncThunk(
  'accountsPayable/createPayment',
  async (payment: Omit<Payment, 'id'>, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 500));
      return { ...payment, id: Date.now() };
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

export const createPurchaseOrder = createAsyncThunk(
  'accountsPayable/createPurchaseOrder',
  async (po: Omit<PurchaseOrder, 'id'>, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 500));
      return { ...po, id: Date.now() };
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

const accountsPayableSlice = createSlice({
  name: 'accountsPayable',
  initialState,
  reducers: {
    setSelectedVendor: (state, action: PayloadAction<Vendor | null>) => {
      state.selectedVendor = action.payload;
    },
    setSelectedInvoice: (state, action: PayloadAction<APInvoice | null>) => {
      state.selectedInvoice = action.payload;
    },
    setSelectedPayment: (state, action: PayloadAction<Payment | null>) => {
      state.selectedPayment = action.payload;
    },
    setSelectedPO: (state, action: PayloadAction<PurchaseOrder | null>) => {
      state.selectedPO = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    addVendor: (state, action: PayloadAction<Vendor>) => {
      state.vendors.push(action.payload);
    },
    updateVendorInState: (state, action: PayloadAction<Vendor>) => {
      const index = state.vendors.findIndex(vendor => vendor.id === action.payload.id);
      if (index !== -1) {
        state.vendors[index] = action.payload;
      }
    },
    removeVendor: (state, action: PayloadAction<number>) => {
      state.vendors = state.vendors.filter(vendor => vendor.id !== action.payload);
    },
    addInvoice: (state, action: PayloadAction<APInvoice>) => {
      state.invoices.push(action.payload);
    },
    updateInvoiceInState: (state, action: PayloadAction<APInvoice>) => {
      const index = state.invoices.findIndex(invoice => invoice.id === action.payload.id);
      if (index !== -1) {
        state.invoices[index] = action.payload;
      }
    },
    removeInvoice: (state, action: PayloadAction<number>) => {
      state.invoices = state.invoices.filter(invoice => invoice.id !== action.payload);
    },
    addPayment: (state, action: PayloadAction<Payment>) => {
      state.payments.push(action.payload);
    },
    updatePaymentInState: (state, action: PayloadAction<Payment>) => {
      const index = state.payments.findIndex(payment => payment.id === action.payload.id);
      if (index !== -1) {
        state.payments[index] = action.payload;
      }
    },
    removePayment: (state, action: PayloadAction<number>) => {
      state.payments = state.payments.filter(payment => payment.id !== action.payload);
    },
    addPurchaseOrder: (state, action: PayloadAction<PurchaseOrder>) => {
      state.purchaseOrders.push(action.payload);
    },
    updatePurchaseOrderInState: (state, action: PayloadAction<PurchaseOrder>) => {
      const index = state.purchaseOrders.findIndex(po => po.id === action.payload.id);
      if (index !== -1) {
        state.purchaseOrders[index] = action.payload;
      }
    },
    removePurchaseOrder: (state, action: PayloadAction<number>) => {
      state.purchaseOrders = state.purchaseOrders.filter(po => po.id !== action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch vendors
      .addCase(fetchVendors.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchVendors.fulfilled, (state, action) => {
        state.loading = false;
        state.vendors = action.payload;
      })
      .addCase(fetchVendors.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch invoices
      .addCase(fetchInvoices.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchInvoices.fulfilled, (state, action) => {
        state.loading = false;
        state.invoices = action.payload;
      })
      .addCase(fetchInvoices.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch payments
      .addCase(fetchPayments.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPayments.fulfilled, (state, action) => {
        state.loading = false;
        state.payments = action.payload;
      })
      .addCase(fetchPayments.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch purchase orders
      .addCase(fetchPurchaseOrders.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPurchaseOrders.fulfilled, (state, action) => {
        state.loading = false;
        state.purchaseOrders = action.payload;
      })
      .addCase(fetchPurchaseOrders.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Create vendor
      .addCase(createVendor.fulfilled, (state, action) => {
        state.vendors.push(action.payload);
      })
      .addCase(createVendor.rejected, (state, action) => {
        state.error = action.payload as string;
      })
      // Create invoice
      .addCase(createInvoice.fulfilled, (state, action) => {
        state.invoices.push(action.payload);
      })
      .addCase(createInvoice.rejected, (state, action) => {
        state.error = action.payload as string;
      })
      // Create payment
      .addCase(createPayment.fulfilled, (state, action) => {
        state.payments.push(action.payload);
      })
      .addCase(createPayment.rejected, (state, action) => {
        state.error = action.payload as string;
      })
      // Create purchase order
      .addCase(createPurchaseOrder.fulfilled, (state, action) => {
        state.purchaseOrders.push(action.payload);
      })
      .addCase(createPurchaseOrder.rejected, (state, action) => {
        state.error = action.payload as string;
      });
  },
});

export const {
  setSelectedVendor,
  setSelectedInvoice,
  setSelectedPayment,
  setSelectedPO,
  clearError,
  addVendor,
  updateVendorInState,
  removeVendor,
  addInvoice,
  updateInvoiceInState,
  removeInvoice,
  addPayment,
  updatePaymentInState,
  removePayment,
  addPurchaseOrder,
  updatePurchaseOrderInState,
  removePurchaseOrder,
} = accountsPayableSlice.actions;

export default accountsPayableSlice.reducer; 