import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

// Types
export interface Customer {
  id: number;
  customerCode: string;
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

export interface ARInvoice {
  id: number;
  invoiceNumber: string;
  customerId: number;
  customerName: string;
  invoiceDate: string;
  dueDate: string;
  amount: number;
  taxAmount: number;
  totalAmount: number;
  status: 'draft' | 'sent' | 'paid' | 'overdue' | 'cancelled';
  description: string;
  reference: string;
  createdBy: string;
  createdAt: string;
  sentAt?: string;
  paidAt?: string;
  lines: ARInvoiceLine[];
}

export interface ARInvoiceLine {
  id: number;
  description: string;
  quantity: number;
  unitPrice: number;
  amount: number;
  taxRate: number;
  taxAmount: number;
  totalAmount: number;
}

export interface Collection {
  id: number;
  collectionNumber: string;
  customerId: number;
  customerName: string;
  collectionDate: string;
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

export interface SalesOrder {
  id: number;
  soNumber: string;
  customerId: number;
  customerName: string;
  orderDate: string;
  expectedDeliveryDate: string;
  totalAmount: number;
  status: 'draft' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled';
  description: string;
  createdBy: string;
  createdAt: string;
  lines: SalesOrderLine[];
}

export interface SalesOrderLine {
  id: number;
  description: string;
  quantity: number;
  unitPrice: number;
  amount: number;
  shippedQuantity: number;
}

export interface AccountsReceivableState {
  customers: Customer[];
  invoices: ARInvoice[];
  collections: Collection[];
  salesOrders: SalesOrder[];
  loading: boolean;
  error: string | null;
  selectedCustomer: Customer | null;
  selectedInvoice: ARInvoice | null;
  selectedCollection: Collection | null;
  selectedSO: SalesOrder | null;
}

const initialState: AccountsReceivableState = {
  customers: [],
  invoices: [],
  collections: [],
  salesOrders: [],
  loading: false,
  error: null,
  selectedCustomer: null,
  selectedInvoice: null,
  selectedCollection: null,
  selectedSO: null,
};

// Async thunks
export const fetchCustomers = createAsyncThunk(
  'accountsReceivable/fetchCustomers',
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

export const fetchARInvoices = createAsyncThunk(
  'accountsReceivable/fetchARInvoices',
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

export const fetchCollections = createAsyncThunk(
  'accountsReceivable/fetchCollections',
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

export const fetchSalesOrders = createAsyncThunk(
  'accountsReceivable/fetchSalesOrders',
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

export const createCustomer = createAsyncThunk(
  'accountsReceivable/createCustomer',
  async (customer: Omit<Customer, 'id'>, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 500));
      return { ...customer, id: Date.now() };
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

export const createARInvoice = createAsyncThunk(
  'accountsReceivable/createARInvoice',
  async (invoice: Omit<ARInvoice, 'id'>, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 500));
      return { ...invoice, id: Date.now() };
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

export const createCollection = createAsyncThunk(
  'accountsReceivable/createCollection',
  async (collection: Omit<Collection, 'id'>, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 500));
      return { ...collection, id: Date.now() };
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

export const createSalesOrder = createAsyncThunk(
  'accountsReceivable/createSalesOrder',
  async (so: Omit<SalesOrder, 'id'>, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 500));
      return { ...so, id: Date.now() };
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

const accountsReceivableSlice = createSlice({
  name: 'accountsReceivable',
  initialState,
  reducers: {
    setSelectedCustomer: (state, action: PayloadAction<Customer | null>) => {
      state.selectedCustomer = action.payload;
    },
    setSelectedInvoice: (state, action: PayloadAction<ARInvoice | null>) => {
      state.selectedInvoice = action.payload;
    },
    setSelectedCollection: (state, action: PayloadAction<Collection | null>) => {
      state.selectedCollection = action.payload;
    },
    setSelectedSO: (state, action: PayloadAction<SalesOrder | null>) => {
      state.selectedSO = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    addCustomer: (state, action: PayloadAction<Customer>) => {
      state.customers.push(action.payload);
    },
    updateCustomerInState: (state, action: PayloadAction<Customer>) => {
      const index = state.customers.findIndex(customer => customer.id === action.payload.id);
      if (index !== -1) {
        state.customers[index] = action.payload;
      }
    },
    removeCustomer: (state, action: PayloadAction<number>) => {
      state.customers = state.customers.filter(customer => customer.id !== action.payload);
    },
    addARInvoice: (state, action: PayloadAction<ARInvoice>) => {
      state.invoices.push(action.payload);
    },
    updateARInvoiceInState: (state, action: PayloadAction<ARInvoice>) => {
      const index = state.invoices.findIndex(invoice => invoice.id === action.payload.id);
      if (index !== -1) {
        state.invoices[index] = action.payload;
      }
    },
    removeARInvoice: (state, action: PayloadAction<number>) => {
      state.invoices = state.invoices.filter(invoice => invoice.id !== action.payload);
    },
    addCollection: (state, action: PayloadAction<Collection>) => {
      state.collections.push(action.payload);
    },
    updateCollectionInState: (state, action: PayloadAction<Collection>) => {
      const index = state.collections.findIndex(collection => collection.id === action.payload.id);
      if (index !== -1) {
        state.collections[index] = action.payload;
      }
    },
    removeCollection: (state, action: PayloadAction<number>) => {
      state.collections = state.collections.filter(collection => collection.id !== action.payload);
    },
    addSalesOrder: (state, action: PayloadAction<SalesOrder>) => {
      state.salesOrders.push(action.payload);
    },
    updateSalesOrderInState: (state, action: PayloadAction<SalesOrder>) => {
      const index = state.salesOrders.findIndex(so => so.id === action.payload.id);
      if (index !== -1) {
        state.salesOrders[index] = action.payload;
      }
    },
    removeSalesOrder: (state, action: PayloadAction<number>) => {
      state.salesOrders = state.salesOrders.filter(so => so.id !== action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch customers
      .addCase(fetchCustomers.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCustomers.fulfilled, (state, action) => {
        state.loading = false;
        state.customers = action.payload;
      })
      .addCase(fetchCustomers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch AR invoices
      .addCase(fetchARInvoices.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchARInvoices.fulfilled, (state, action) => {
        state.loading = false;
        state.invoices = action.payload;
      })
      .addCase(fetchARInvoices.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch collections
      .addCase(fetchCollections.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCollections.fulfilled, (state, action) => {
        state.loading = false;
        state.collections = action.payload;
      })
      .addCase(fetchCollections.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch sales orders
      .addCase(fetchSalesOrders.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSalesOrders.fulfilled, (state, action) => {
        state.loading = false;
        state.salesOrders = action.payload;
      })
      .addCase(fetchSalesOrders.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Create customer
      .addCase(createCustomer.fulfilled, (state, action) => {
        state.customers.push(action.payload);
      })
      .addCase(createCustomer.rejected, (state, action) => {
        state.error = action.payload as string;
      })
      // Create AR invoice
      .addCase(createARInvoice.fulfilled, (state, action) => {
        state.invoices.push(action.payload);
      })
      .addCase(createARInvoice.rejected, (state, action) => {
        state.error = action.payload as string;
      })
      // Create collection
      .addCase(createCollection.fulfilled, (state, action) => {
        state.collections.push(action.payload);
      })
      .addCase(createCollection.rejected, (state, action) => {
        state.error = action.payload as string;
      })
      // Create sales order
      .addCase(createSalesOrder.fulfilled, (state, action) => {
        state.salesOrders.push(action.payload);
      })
      .addCase(createSalesOrder.rejected, (state, action) => {
        state.error = action.payload as string;
      });
  },
});

export const {
  setSelectedCustomer,
  setSelectedInvoice,
  setSelectedCollection,
  setSelectedSO,
  clearError,
  addCustomer,
  updateCustomerInState,
  removeCustomer,
  addARInvoice,
  updateARInvoiceInState,
  removeARInvoice,
  addCollection,
  updateCollectionInState,
  removeCollection,
  addSalesOrder,
  updateSalesOrderInState,
  removeSalesOrder,
} = accountsReceivableSlice.actions;

 