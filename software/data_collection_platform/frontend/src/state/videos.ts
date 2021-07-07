import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";
import { VideoInfo } from "../types";
import api from "../api";

export const fetch = createAsyncThunk("videos/fetch", api.fetchVideos);

const videos = createSlice({
  name: "videos",
  initialState: {
    videos: [] as VideoInfo[],
    videosToWatch: [] as VideoInfo[],
  },
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
  extraReducers: (builder) => {
    builder.addCase(fetch.fulfilled, (st, action) => {
      st.videos = action.payload;
    });
  },
});
export default videos.reducer;

export const { setVideos, setVideosToWatch } = videos.actions;
