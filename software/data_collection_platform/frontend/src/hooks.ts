import {
  TypedUseSelectorHook,
  useDispatch as useDispatch_,
  useSelector as useSelector_,
} from "react-redux";
import type { State, Dispatch } from "./store";

export const useDispatch = () => useDispatch_<Dispatch>();
export const useSelector: TypedUseSelectorHook<State> = useSelector_;
