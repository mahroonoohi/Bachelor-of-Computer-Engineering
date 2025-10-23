import { createSlice } from "@reduxjs/toolkit";

const userMediaLinksSlice = createSlice({
  name: "userMediaLink",
  initialState: { userMediaLinks: [], userMediaLinksNum: 0 },
  reducers: {
    addUserMediaLink(state, action) {
      const newItem = action.payload;
      const existingItem = state.userMediaLinks.find(
        (item) => item.title === newItem.title
      );

      if (
        (state.userMediaLinksNum === 0 || !existingItem) &&
        (newItem.details.startsWith("https://") ||
          newItem.details.startsWith("http://"))
      ) {
        state.userMediaLinksNum++;
        state.userMediaLinks.push({
          uuid: newItem.uuid,
          title: newItem.title,
          details: newItem.details,
        });
      }
    },
    deleteUserMediaLink(state, action) {
      const newItem = action.payload;
      const existingItem = state.userMediaLinks.find(
        (item) => item.title === newItem.title
      );

      if (existingItem) {
        state.userMediaLinksNum--;
        state.userMediaLinks = state.userMediaLinks.filter(
          (task) => task.title !== newItem.title
        );
      }
    },
    deleteAll(state, action) {
      state.financialSteps = [];
      state.financialStepsNum = 0;
    },
  },
});

export const userMediaLinksActions = userMediaLinksSlice.actions;

export const userMediaLinksReducer = userMediaLinksSlice.reducer;
