import { createSlice } from "@reduxjs/toolkit";

const attachedFilesSlice = createSlice({
  name: "attachedFiles",
  initialState: { attachedFiles: [], attachedFilesNum: 0 },
  reducers: {
    addAttachedFiles(state, action) {
      const newItem = action.payload;
      const existingItem = state.attachedFiles.find(
        (item) => item.uuid === newItem.uuid
      );

      if (!existingItem) {
        state.attachedFilesNum++;
        state.attachedFiles.push({
          uuid: newItem.uuid,
          name: newItem.name,
          type: newItem.type,
        });
      }
    },
    deleteAttachedFiles(state, action) {
      const newItem = action.payload;
      const existingItem = state.attachedFiles.find(
        (item) => item.uuid === newItem.uuid
      );

      if (existingItem) {
        state.attachedFilesNum--;
        state.attachedFiles = state.attachedFiles.filter(
          (task) => task.uuid !== newItem.uuid
        );
      }
    },
    deleteAllAttachedFiles(state, action) {
      state.attachedFiles = [];
      state.attachedFilesNum = 0;
    },
  },
});

export const attachedFilesActions = attachedFilesSlice.actions;

export const attachedFilesReducer = attachedFilesSlice.reducer;
