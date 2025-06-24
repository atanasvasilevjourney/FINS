import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

// Types
export interface Account {
  id: number;
  accountCode: string;
  accountName: string;
  accountType: string;
  accountCategory: string;
  normalBalance: string;
  isActive: boolean;
  description: string;
  parentAccountId?: number;
  balance?: number;
}

export interface JournalEntry {
  id: number;
  entryNumber: string;
  date: string;
  description: string;
  reference: string;
  status: 'draft' | 'posted' | 'void';
  totalDebit: number;
  totalCredit: number;
  createdBy: string;
  createdAt: string;
  postedAt?: string;
  lines: JournalEntryLine[];
}

export interface JournalEntryLine {
  id: number;
  accountId: number;
  accountCode: string;
  accountName: string;
  description: string;
  debit: number;
  credit: number;
}

export interface GeneralLedgerState {
  accounts: Account[];
  journalEntries: JournalEntry[];
  loading: boolean;
  error: string | null;
  selectedAccount: Account | null;
  selectedEntry: JournalEntry | null;
}

const initialState: GeneralLedgerState = {
  accounts: [],
  journalEntries: [],
  loading: false,
  error: null,
  selectedAccount: null,
  selectedEntry: null,
};

// Async thunks
export const fetchAccounts = createAsyncThunk(
  'generalLedger/fetchAccounts',
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

export const fetchJournalEntries = createAsyncThunk(
  'generalLedger/fetchJournalEntries',
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

export const createAccount = createAsyncThunk(
  'generalLedger/createAccount',
  async (account: Omit<Account, 'id'>, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 500));
      return { ...account, id: Date.now() };
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

export const updateAccount = createAsyncThunk(
  'generalLedger/updateAccount',
  async (account: Account, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 500));
      return account;
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

export const createJournalEntry = createAsyncThunk(
  'generalLedger/createJournalEntry',
  async (entry: Omit<JournalEntry, 'id'>, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 500));
      return { ...entry, id: Date.now() };
    } catch (error: any) {
      return rejectWithValue(error.message);
    }
  }
);

const generalLedgerSlice = createSlice({
  name: 'generalLedger',
  initialState,
  reducers: {
    setSelectedAccount: (state, action: PayloadAction<Account | null>) => {
      state.selectedAccount = action.payload;
    },
    setSelectedEntry: (state, action: PayloadAction<JournalEntry | null>) => {
      state.selectedEntry = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    addAccount: (state, action: PayloadAction<Account>) => {
      state.accounts.push(action.payload);
    },
    updateAccountInState: (state, action: PayloadAction<Account>) => {
      const index = state.accounts.findIndex(account => account.id === action.payload.id);
      if (index !== -1) {
        state.accounts[index] = action.payload;
      }
    },
    removeAccount: (state, action: PayloadAction<number>) => {
      state.accounts = state.accounts.filter(account => account.id !== action.payload);
    },
    addJournalEntry: (state, action: PayloadAction<JournalEntry>) => {
      state.journalEntries.push(action.payload);
    },
    updateJournalEntryInState: (state, action: PayloadAction<JournalEntry>) => {
      const index = state.journalEntries.findIndex(entry => entry.id === action.payload.id);
      if (index !== -1) {
        state.journalEntries[index] = action.payload;
      }
    },
    removeJournalEntry: (state, action: PayloadAction<number>) => {
      state.journalEntries = state.journalEntries.filter(entry => entry.id !== action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch accounts
      .addCase(fetchAccounts.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAccounts.fulfilled, (state, action) => {
        state.loading = false;
        state.accounts = action.payload;
      })
      .addCase(fetchAccounts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch journal entries
      .addCase(fetchJournalEntries.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchJournalEntries.fulfilled, (state, action) => {
        state.loading = false;
        state.journalEntries = action.payload;
      })
      .addCase(fetchJournalEntries.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Create account
      .addCase(createAccount.fulfilled, (state, action) => {
        state.accounts.push(action.payload);
      })
      .addCase(createAccount.rejected, (state, action) => {
        state.error = action.payload as string;
      })
      // Update account
      .addCase(updateAccount.fulfilled, (state, action) => {
        const index = state.accounts.findIndex(account => account.id === action.payload.id);
        if (index !== -1) {
          state.accounts[index] = action.payload;
        }
      })
      .addCase(updateAccount.rejected, (state, action) => {
        state.error = action.payload as string;
      })
      // Create journal entry
      .addCase(createJournalEntry.fulfilled, (state, action) => {
        state.journalEntries.push(action.payload);
      })
      .addCase(createJournalEntry.rejected, (state, action) => {
        state.error = action.payload as string;
      });
  },
});

export const {
  setSelectedAccount,
  setSelectedEntry,
  clearError,
  addAccount,
  updateAccountInState,
  removeAccount,
  addJournalEntry,
  updateJournalEntryInState,
  removeJournalEntry,
} = generalLedgerSlice.actions;

export default generalLedgerSlice.reducer; 