import { configureStore } from "@reduxjs/toolkit";
import reducer from "./state";

const store = configureStore({
  reducer,
  devTools: true,
});

export type State = ReturnType<typeof store.getState>;
export type Dispatch = typeof store.dispatch;
export default store;
