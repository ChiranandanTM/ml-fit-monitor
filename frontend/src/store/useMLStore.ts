import { create } from "zustand";

export const useMLStore = create<any>((set) => ({
  results: null,
  lastUploadedFile: null,
  agentTrace: null,
  setResults: (data: any) => set({ results: data }),
  setLastUploadedFile: (file: File | null) => set({ lastUploadedFile: file }),
  setAgentTrace: (trace: any) => set({ agentTrace: trace })
}));
