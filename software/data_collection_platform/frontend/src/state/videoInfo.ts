import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { VideoInfo } from "../types";

const initialState = {
  videos: [] as VideoInfo[],
  videosToWatch: [] as VideoInfo[],
};

const Videos = createSlice({
  name: "videoInfo",
  initialState: initialState,
  reducers: {
    setVideos: (state, action: PayloadAction<VideoInfo[]>) => ({
      ...state,
      videos: action.payload,
    }),
    setVideosToWatch: (state, action: PayloadAction<VideoInfo[]>) => ({
      ...state,
      videosToWatch: action.payload,
    }),
  },
});

export default Videos;
