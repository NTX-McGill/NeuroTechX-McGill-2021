import { createSlice, PayloadAction } from "@reduxjs/toolkit";

type Period = [string, string];

const anxiousPeriods = createSlice({
  name: "anxiousPeriods",
  initialState: [] as Period[],
  reducers: {
    clear: () => [],
    addPeriod: (state, action: PayloadAction<Period>) => [
      ...state,
      action.payload,
    ],
  },
});
export default anxiousPeriods;
