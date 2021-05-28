import { configureStore } from "@reduxjs/toolkit";

const store = configureStore({
  reducer: {
    // Placeholder reducer, remove once we've added one.
    placeholder: (st = null) => st,
  },
  devTools: true,
});

export type State = ReturnType<typeof store.getState>;
export type Dispatch = typeof store.dispatch;
export default store;
