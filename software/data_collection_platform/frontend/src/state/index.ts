import { configureStore } from "@reduxjs/toolkit";

// Import reducers and default export the store.
import videos from "./videos";

const store = configureStore({
  reducer: {
    videos,
  },
  devTools: true,
});
export default store;

// Export actions.
export * as videos from "./videos";
