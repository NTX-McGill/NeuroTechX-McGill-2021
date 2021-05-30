import anxiousPeriodsSlice from "./anxiousPeriods";

export const anxiousPeriods = anxiousPeriodsSlice.actions;

const reducer = {
  anxiousPeriods: anxiousPeriodsSlice.reducer,
};
export default reducer;
