import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

// Types
export interface Supplier {
  id: number;
  supplierCode: string;
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
  certifications: string[];
}

export interface PurchaseRequisition {
  id: number;
  prNumber: string;
  requesterId: number;
  requesterName: string;
  department: string;
  requestDate: string;
  requiredDate: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  status: 'draft' | 'submitted' | 'approved' | 'rejected' | 'converted';
  totalAmount: number;
  description: string;
  justification: string;
  createdBy: string;
  createdAt: string;
  approvedBy?: string;
  approvedAt?: string;
  lines: PurchaseRequisitionLine[];
}

export interface PurchaseRequisitionLine {
  id: number;
  description: string;
  quantity: number;
  unitPrice: number;
  amount: number;
  specifications: string;
  preferredSupplier?: string;
}

export interface RFQ {
  id: number;
  rfqNumber: string;
  title: string;
  description: string;
  issueDate: string;
  dueDate: string;
  status: 'draft' | 'published' | 'closed' | 'awarded' | 'cancelled';
  category: string;
  estimatedValue: number;
  createdBy: string;
  createdAt: string;
  publishedAt?: string;
  closedAt?: string;
  suppliers: RFQSupplier[];
  requirements: RFQRequirement[];
}

export interface RFQSupplier {
  id: number;
  supplierId: number;
  supplierName: string;
  status: 'invited' | 'responded' | 'declined' | 'awarded';
  responseDate?: string;
  bidAmount?: number;
  technicalScore?: number;
  commercialScore?: number;
  totalScore?: number;
}

export interface RFQRequirement {
  id: number;
  description: string;
  quantity: number;
  unit: string;
  specifications: string;
  isMandatory: boolean;
}

export interface Contract {
  id: number;
  contractNumber: string;
  title: string;
  supplierId: number;
  supplierName: string;
  contractType: 'goods' | 'services' | 'mixed';
  startDate: string;
  endDate: string;
  totalValue: number;
  status: 'draft' | 'active' | 'expired' | 'terminated' | 'renewed';
  description: string;
  terms: string;
  createdBy: string;
  createdAt: string;
  signedBy?: string;
  signedAt?: string;
  lines: ContractLine[];
}

export interface ContractLine {
  id: number;
  description: string;
  quantity: number;
  unitPrice: number;
  amount: number;
  deliverySchedule: string;
  specifications: string;
}

export interface ProcurementState {
  suppliers: Supplier[];
  purchaseRequisitions: PurchaseRequisition[];
  rfqs: RFQ[];
  contracts: Contract[];
  loading: boolean;
  error: string | null;
  selectedSupplier: Supplier | null;
  selectedPR: PurchaseRequisition | null;
  selectedRFQ: RFQ | null;
  selectedContract: Contract | null;
}

const initialState: ProcurementState = {
  suppliers: [],
  purchaseRequisitions: [],
  rfqs: [],
  contracts: [],
  loading: false,
  error: null,
  selectedSupplier: null,
  selectedPR: null,
  selectedRFQ: null,
  selectedContract: null,
};

// Async thunks
export const fetchSuppliers = createAsyncThunk(
  'procurement/fetchSuppliers',
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

export const fetchPurchaseRequisitions = createAsyncThunk(
  'procurement/fetchPurchaseRequisitions',
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

export const fetchRFQs = createAsyncThunk(
  'procurement/fetchRFQs',
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

export const fetchContracts = createAsyncThunk(
  'procurement/fetchContracts',
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

export const createSupplier = createAsyncThunk(
  'procurement/createSupplier',
  async (supplier: Omit<Supplier, 'id'>, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 500));
      return { ...supplier, id: Date.now() };
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

export const createPurchaseRequisition = createAsyncThunk(
  'procurement/createPurchaseRequisition',
  async (pr: Omit<PurchaseRequisition, 'id'>, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 500));
      return { ...pr, id: Date.now() };
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

export const createRFQ = createAsyncThunk(
  'procurement/createRFQ',
  async (rfq: Omit<RFQ, 'id'>, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 500));
      return { ...rfq, id: Date.now() };
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

export const createContract = createAsyncThunk(
  'procurement/createContract',
  async (contract: Omit<Contract, 'id'>, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 500));
      return { ...contract, id: Date.now() };
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

const procurementSlice = createSlice({
  name: 'procurement',
  initialState,
  reducers: {
    setSelectedSupplier: (state, action: PayloadAction<Supplier | null>) => {
      state.selectedSupplier = action.payload;
    },
    setSelectedPR: (state, action: PayloadAction<PurchaseRequisition | null>) => {
      state.selectedPR = action.payload;
    },
    setSelectedRFQ: (state, action: PayloadAction<RFQ | null>) => {
      state.selectedRFQ = action.payload;
    },
    setSelectedContract: (state, action: PayloadAction<Contract | null>) => {
      state.selectedContract = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    addSupplier: (state, action: PayloadAction<Supplier>) => {
      state.suppliers.push(action.payload);
    },
    updateSupplierInState: (state, action: PayloadAction<Supplier>) => {
      const index = state.suppliers.findIndex(supplier => supplier.id === action.payload.id);
      if (index !== -1) {
        state.suppliers[index] = action.payload;
      }
    },
    removeSupplier: (state, action: PayloadAction<number>) => {
      state.suppliers = state.suppliers.filter(supplier => supplier.id !== action.payload);
    },
    addPurchaseRequisition: (state, action: PayloadAction<PurchaseRequisition>) => {
      state.purchaseRequisitions.push(action.payload);
    },
    updatePurchaseRequisitionInState: (state, action: PayloadAction<PurchaseRequisition>) => {
      const index = state.purchaseRequisitions.findIndex(pr => pr.id === action.payload.id);
      if (index !== -1) {
        state.purchaseRequisitions[index] = action.payload;
      }
    },
    removePurchaseRequisition: (state, action: PayloadAction<number>) => {
      state.purchaseRequisitions = state.purchaseRequisitions.filter(pr => pr.id !== action.payload);
    },
    addRFQ: (state, action: PayloadAction<RFQ>) => {
      state.rfqs.push(action.payload);
    },
    updateRFQInState: (state, action: PayloadAction<RFQ>) => {
      const index = state.rfqs.findIndex(rfq => rfq.id === action.payload.id);
      if (index !== -1) {
        state.rfqs[index] = action.payload;
      }
    },
    removeRFQ: (state, action: PayloadAction<number>) => {
      state.rfqs = state.rfqs.filter(rfq => rfq.id !== action.payload);
    },
    addContract: (state, action: PayloadAction<Contract>) => {
      state.contracts.push(action.payload);
    },
    updateContractInState: (state, action: PayloadAction<Contract>) => {
      const index = state.contracts.findIndex(contract => contract.id === action.payload.id);
      if (index !== -1) {
        state.contracts[index] = action.payload;
      }
    },
    removeContract: (state, action: PayloadAction<number>) => {
      state.contracts = state.contracts.filter(contract => contract.id !== action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch suppliers
      .addCase(fetchSuppliers.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSuppliers.fulfilled, (state, action) => {
        state.loading = false;
        state.suppliers = action.payload;
      })
      .addCase(fetchSuppliers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch purchase requisitions
      .addCase(fetchPurchaseRequisitions.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPurchaseRequisitions.fulfilled, (state, action) => {
        state.loading = false;
        state.purchaseRequisitions = action.payload;
      })
      .addCase(fetchPurchaseRequisitions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch RFQs
      .addCase(fetchRFQs.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchRFQs.fulfilled, (state, action) => {
        state.loading = false;
        state.rfqs = action.payload;
      })
      .addCase(fetchRFQs.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch contracts
      .addCase(fetchContracts.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchContracts.fulfilled, (state, action) => {
        state.loading = false;
        state.contracts = action.payload;
      })
      .addCase(fetchContracts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Create supplier
      .addCase(createSupplier.fulfilled, (state, action) => {
        state.suppliers.push(action.payload);
      })
      .addCase(createSupplier.rejected, (state, action) => {
        state.error = action.payload as string;
      })
      // Create purchase requisition
      .addCase(createPurchaseRequisition.fulfilled, (state, action) => {
        state.purchaseRequisitions.push(action.payload);
      })
      .addCase(createPurchaseRequisition.rejected, (state, action) => {
        state.error = action.payload as string;
      })
      // Create RFQ
      .addCase(createRFQ.fulfilled, (state, action) => {
        state.rfqs.push(action.payload);
      })
      .addCase(createRFQ.rejected, (state, action) => {
        state.error = action.payload as string;
      })
      // Create contract
      .addCase(createContract.fulfilled, (state, action) => {
        state.contracts.push(action.payload);
      })
      .addCase(createContract.rejected, (state, action) => {
        state.error = action.payload as string;
      });
  },
});

export const {
  setSelectedSupplier,
  setSelectedPR,
  setSelectedRFQ,
  setSelectedContract,
  clearError,
  addSupplier,
  updateSupplierInState,
  removeSupplier,
  addPurchaseRequisition,
  updatePurchaseRequisitionInState,
  removePurchaseRequisition,
  addRFQ,
  updateRFQInState,
  removeRFQ,
  addContract,
  updateContractInState,
  removeContract,
} = procurementSlice.actions;

export default procurementSlice.reducer; 