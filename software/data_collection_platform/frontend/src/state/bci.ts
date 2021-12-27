import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";
import { ProcessId, ThunkApiConfig } from "../types";
import api from "../api";

export const ready = createAsyncThunk<boolean, void, ThunkApiConfig>(
  "bci/ready",
  async (_, { getState }) => {
    const { process_id } = getState().bci;
    if (!process_id) return false;
    return await api.openBciReady(process_id);
  },
);

// Start the BCI device using api.openBciStart(), and after
// retrieving the new process_id check if the device is ready.
export const start = createAsyncThunk<ProcessId, void, ThunkApiConfig>(
  "bci/start",
  async (_, { dispatch }) => {
    const process_id = await api.openBciStart();
    dispatch(bci.actions.setProcessId(process_id));
    dispatch(ready());
    return process_id;
  },
);

export const stop = createAsyncThunk<ProcessId, void, ThunkApiConfig>(
  "bci/stop",
  async (_, { getState }) => {
    const { process_id } = getState().bci;
    if (process_id) return await api.openBciStop(process_id);
  },
);

const bci = createSlice({
  name: "bci",
  initialState: {
    process_id: null as ProcessId | null,
    pending: false as boolean,
    ready: false as boolean,
  },
  reducers: {
    setProcessId: (st, action: PayloadAction<ProcessId>) => ({
      ...st,
      process_id: action.payload,
      pending: false,
      ready: false,
    }),
  },
  extraReducers: (builder) => {
    builder.addCase(stop.fulfilled, (st) => {
      st.process_id = null;
    });
    builder.addCase(ready.pending, (st) => {
      st.pending = true;
    });
    builder.addCase(ready.fulfilled, (st, action) => {
      st.pending = false;
      if (action.payload) st.ready = true;
    });
  },
});
export default bci.reducer;
