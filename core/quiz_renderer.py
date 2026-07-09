"""Quiz rendering helpers."""

from __future__ import annotations

import streamlit as st

from core.i18n import t


def render_quiz_items(quiz_items: list[dict], key_prefix: str) -> None:
    total = len(quiz_items)
    if total == 0:
        return

    if st.button(t("quiz_reset"), key=f"{key_prefix}_quiz_reset"):
        for index in range(1, total + 1):
            st.session_state.pop(f"{key_prefix}_quiz_{index}", None)
            st.session_state.pop(f"{key_prefix}_quiz_checked_{index}", None)
        st.rerun()

    for index, quiz in enumerate(quiz_items, start=1):
        st.markdown(f"### {index}. {quiz['question']}")
        answer = st.radio(
            t("answer_select"),
            quiz["options"],
            index=None,
            key=f"{key_prefix}_quiz_{index}",
            label_visibility="collapsed",
        )
        checked_key = f"{key_prefix}_quiz_checked_{index}"
        if st.button(t("quiz_check"), key=f"{key_prefix}_quiz_check_{index}"):
            if answer is None:
                st.warning(t("quiz_select_prompt"))
            else:
                st.session_state[checked_key] = answer

        checked_answer = st.session_state.get(checked_key)
        if checked_answer == answer == quiz["answer"]:
            st.success(quiz["correct"])
        elif checked_answer is not None and checked_answer == answer:
            if answer is not None:
                st.error(quiz["wrong"])

        if index < total:
            st.divider()

    checked_answers = []
    for index in range(1, total + 1):
        selected = st.session_state.get(f"{key_prefix}_quiz_{index}")
        checked = st.session_state.get(f"{key_prefix}_quiz_checked_{index}")
        checked_answers.append(checked if checked == selected else None)
    answered = sum(answer is not None for answer in checked_answers)
    correct = sum(
        checked_answers[index - 1] == quiz["answer"]
        for index, quiz in enumerate(quiz_items, start=1)
    )
    st.progress(
        correct / total,
        text=t("quiz_progress").format(answered=answered, total=total, correct=correct),
    )
