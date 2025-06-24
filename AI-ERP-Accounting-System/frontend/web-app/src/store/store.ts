import { configureStore } from '@reduxjs/toolkit';
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';

// Slices
import authSlice from './slices/authSlice';
import uiSlice from './slices/uiSlice';
import generalLedgerSlice from './slices/generalLedgerSlice';
import accountsPayableSlice from './slices/accountsPayableSlice';
import accountsReceivableSlice from './slices/accountsReceivableSlice';
import procurementSlice from './slices/procurementSlice';

export const store = configureStore({
  reducer: {
    auth: authSlice,
    ui: uiSlice,
    generalLedger: generalLedgerSlice,
    accountsPayable: accountsPayableSlice,
    accountsReceivable: accountsReceivableSlice,
    procurement: procurementSlice,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Use throughout your app instead of plain `useDispatch` and `useSelector`
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector; 