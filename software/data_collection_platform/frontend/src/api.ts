import { FeedbackValue, VideoInfo, ProcessId } from "./types";

const query = async (
  endpoint: string,
  method: string,
  data?: object,
): Promise<any> => {
  if (process.env.REACT_APP_SERVER_URL === undefined)
    throw new Error("$REACT_APP_SERVER_URL is undefined");

  const url = `${process.env.REACT_APP_SERVER_URL}${endpoint}`;
  const resp = await fetch(url, {
    method,
    headers: {
      "Content-Type": "application/json",
    },
    body: data && JSON.stringify(data),
  });
  return await resp.json();
};

// Constructs an Api object that we can use to call the endpoints
// specified above.
//
// e.g.
//   api.anxiousStart({ ... })
//   api.anxiousStop({ ... })
//
// prettier-ignore
const api = {
  videoStart: () =>
    query("/api/video/start", "PUT"),

  videoStop: () =>
    query("/api/video/stop", "PUT"),

  anxiousStart: () =>
    query("/api/anxious/start", "PUT"),

  anxiousStop: () =>
    query("/api/anxious/stop", "PUT"),

  sendFeedback: (d: { video_id: number; stress_level: FeedbackValue }) =>
    query("/api/feedback", "POST", d),

  fetchVideos: () =>
    query("/api/videos", "GET")
    .then((d) => d.data as VideoInfo[]),

  openBciStart: () =>
    query("/api/openbci/start", "POST")
    .then((d) => d.data.pid as ProcessId),

  openBciStop: (p: ProcessId) =>
    query(`/api/openbci/${p}/stop`, "POST"),

  openBciReady: (p: ProcessId) =>
    query(`/api/openbci/${p}/ready`, "GET")
    .then((d) => d.data as boolean),
};
export default api;
