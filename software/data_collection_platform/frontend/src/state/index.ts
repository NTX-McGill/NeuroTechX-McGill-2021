import anxiousPeriodsSlice from "./anxiousPeriods";
import VideosSlice from "./videoInfo";

export const anxiousPeriods = anxiousPeriodsSlice.actions;
export const videos = VideosSlice.actions;

const reducer = {
  anxiousPeriods: anxiousPeriodsSlice.reducer,
  videos: VideosSlice.reducer,
};
export default reducer;
