"use client";

import {useCallback, useEffect, useRef, useState} from "react";

export type RecorderState = "idle" | "recording" | "ready" | "error";

export function useRecorder(maxSeconds = 10) {
  const [state, setState] = useState<RecorderState>("idle");
  const [blob, setBlob] = useState<Blob | null>(null);
  const [durationMs, setDurationMs] = useState(0);
  const mediaStreamRef = useRef<MediaStream | null>(null);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<BlobPart[]>([]);
  const timerRef = useRef<any>(null);
  const startedAtRef = useRef<number>(0);

  useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
      if (recorderRef.current && recorderRef.current.state !== "inactive") {
        recorderRef.current.stop();
      }
      mediaStreamRef.current?.getTracks().forEach((t) => t.stop());
    };
  }, []);

  const start = useCallback(async () => {
    try {
      setBlob(null);
      setDurationMs(0);
      const stream = await navigator.mediaDevices.getUserMedia({audio: true});
      mediaStreamRef.current = stream;
      const rec = new MediaRecorder(stream, {mimeType: "audio/webm"});
      recorderRef.current = rec;
      chunksRef.current = [];
      rec.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) chunksRef.current.push(e.data);
      };
      rec.onstop = () => {
        const b = new Blob(chunksRef.current, {type: "audio/webm"});
        setBlob(b);
        const elapsed = Date.now() - startedAtRef.current;
        setDurationMs(elapsed);
        setState("ready");
        stream.getTracks().forEach((t) => t.stop());
      };
      rec.start();
      startedAtRef.current = Date.now();
      setState("recording");
      timerRef.current = setTimeout(() => {
        if (rec.state !== "inactive") rec.stop();
      }, maxSeconds * 1000);
    } catch (e) {
      console.error("Recorder start failed", e);
      setState("error");
    }
  }, [maxSeconds]);

  const stop = useCallback(() => {
    if (recorderRef.current && recorderRef.current.state !== "inactive") {
      recorderRef.current.stop();
    }
  }, []);

  const reset = useCallback(() => {
    setState("idle");
    setBlob(null);
    setDurationMs(0);
  }, []);

  return {state, blob, durationMs, start, stop, reset};
}
