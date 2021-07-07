import store from './state';
export type State = ReturnType<typeof store.getState>;
export type Dispatch = typeof store.dispatch;

export interface VideoInfo {
  end?: number;
  id: number;
  is_stressful: boolean;
  keywords: string[];
  start?: number;
  youtube_id: string;
  youtube_url: string;
}

export type FeedbackValue = 1 | 2 | 3;
