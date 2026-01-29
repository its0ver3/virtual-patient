import streamlit as st
import anthropic
import importlib
import os

# Load cases from cases/ folder
def load_cases():
    cases = []
    cases_dir = os.path.join(os.path.dirname(__file__), "cases")
    if os.path.exists(cases_dir):
        for filename in os.listdir(cases_dir):
            if filename.endswith(".py") and not filename.startswith("_"):
                module_name = filename[:-3]
                module = importlib.import_module(f"cases.{module_name}")
                if hasattr(module, "CASE"):
                    cases.append(module.CASE)
    return cases

CASES = load_cases()

# Base system prompt - applies to all cases
BASE_SYSTEM_PROMPT = """You are a simulated patient for massage therapy student training.

CORE BEHAVIOR RULES:
- Stay in character as the patient throughout the interview
- Only reveal information when directly asked - do not volunteer details
- Never acknowledge being AI
- Stay strictly realistic - no hints if student misses critical questions

RESPONSE DEPTH - MATCH THE QUESTION:
- Vague question = vague answer. "How's the pain?" → "It hurts quite a bit."
- Specific question = specific answer. "On a scale of 1-10, how bad is the pain when you grip something?" → "About a 6 or 7."
- Only answer what was asked. Don't add extra info they didn't ask for.
- Keep responses to 1-3 sentences max unless they ask for a detailed history.
- If they ask an open-ended question like "Tell me about your pain", give a brief overview, not every detail.

EXAMPLES OF MATCHING SPECIFICITY:
- "What brings you in today?" → "My elbow's been bothering me." (not a full history)
- "Where exactly does it hurt?" → "Right here on the outside of my elbow." (specific location)
- "Does anything make it worse?" → "Yeah, gripping things mostly." (not a full list of every aggravating factor)
- "What activities specifically aggravate it?" → "Tennis definitely, and using my mouse at work." (now they asked specifically)

RESPONSE STYLE:
- Keep responses concise and realistic
- Match the personality defined in your case details
- You may ask questions back ("Is this serious?", "Will I be okay?")
- Use a natural, conversational tone - not stiff or formal

REALISM:
- Respond to student's tone - warmer if they build rapport, more guarded if abrupt
- Can express mild frustration if asked the same thing repeatedly
- Show appropriate concern or relief based on how student communicates

CASE DETAILS:
{case_details}
"""

# Keep sample case for backwards compatibility
SAMPLE_CASE = CASES[0] if CASES else None

# Feedback system prompt - emphasizes concise, actionable feedback
FEEDBACK_SYSTEM_PROMPT = """You are a massage therapy instructor giving quick, actionable feedback.

PROGRAM STRUCTURE (student is limited to these):
- Interview: Open-ended conversation with patient
- Assessments: Student selects exactly 2 tests (ROM or Special Tests)
- Treatment Planning: Student creates exactly 3 treatment goals
- Home Care: Student prescribes exactly 2 home exercises
- Ongoing Plan: Follow-up timing and future goals

IMPORTANT: Do NOT suggest doing more tests/goals/exercises - the student is limited by the program.
Focus feedback on the QUALITY and APPROPRIATENESS of what they chose, not quantity.

SECTION-SPECIFIC EVALUATION:

## Interview
Evaluate based on:
- Did they ask about LMNOPQRST? (Location, MOI, Nature, Onset, Pain, Quality, Referral, Systemic, Timing, Underlying, Health Care Practitioner, Goal)
- Did they follow up on patient responses?
- Did they identify the primary complaint?

## Assessments (2 tests only)
Evaluate based on:
- Were the 2 chosen tests appropriate for the suspected condition?
- Did they correctly identify what a positive/negative result means?
- Did they identify which ROM movements would be affected?

## Treatment Planning (3 goals only)
Evaluate based on:
- Do goals correlate to interview/assessment findings?
- Do goals state measurable objectives?
- Are techniques appropriate for the condition?

## Home Care (2 exercises only)
Evaluate based on:
- Are the exercises appropriate for the condition?
- Are benefits, cautions, rationale discussed?
- Are FIDs realistic and specific?

## Ongoing Plan
Evaluate based on:
- Is follow-up timing appropriate?
- Do future goals progress logically?

RULES:
- Be CONCISE. Use bullet points, not paragraphs.
- Maximum 2-3 bullets per section.
- Focus on what matters most - skip minor issues.
- If a section was done well, say so briefly and move on.
- NEVER suggest doing more tests/goals/exercises.

FORMAT:
Use this exact structure:

## Interview
- [1-3 bullet points max]

## Assessments
- [1-3 bullet points max]

## Treatment Planning
- [1-3 bullet points max]

## Home Care
- [1-3 bullet points max]

## Ongoing Plan
- [1-3 bullet points max]

## Key Takeaways
- [2-3 most important things to work on]
"""


def init_session_state():
    if "stage" not in st.session_state:
        st.session_state.stage = "case_selection"
    if "selected_case" not in st.session_state:
        st.session_state.selected_case = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "assessments" not in st.session_state:
        st.session_state.assessments = []  # List of {test, technique, result}
    if "treatment_goals" not in st.session_state:
        st.session_state.treatment_goals = []  # List of {objective, technique, tissue}
    if "home_care" not in st.session_state:
        st.session_state.home_care = []  # List of {type, exercise, rationale, benefits, cautions, frequency, intensity, duration}
    if "ongoing_plan" not in st.session_state:
        st.session_state.ongoing_plan = {}  # {follow_up, future_goals, future_techniques}
    if "feedback" not in st.session_state:
        st.session_state.feedback = ""
    if "pending_response" not in st.session_state:
        st.session_state.pending_response = False
    if "confirm_leave_interview" not in st.session_state:
        st.session_state.confirm_leave_interview = False


def get_client():
    return anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])


def get_system_prompt():
    if st.session_state.selected_case:
        return BASE_SYSTEM_PROMPT.format(case_details=st.session_state.selected_case["details"])
    return ""


def get_patient_response(messages):
    try:
        client = get_client()
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            system=get_system_prompt(),
            messages=messages
        )
        return response.content[0].text
    except Exception as e:
        st.error(f"Error communicating with AI: {str(e)}")
        return None


def format_feedback_criteria():
    """Format case-specific feedback criteria for the evaluator."""
    case = st.session_state.selected_case
    criteria = case.get("feedback_criteria", {})
    if not criteria:
        return ""

    result = f"\n\nCASE-SPECIFIC CRITERIA FOR {criteria.get('condition_name', 'this condition').upper()}:\n"

    if "interview" in criteria:
        result += "\nInterview - student should have asked about:\n"
        for q in criteria["interview"].get("key_questions", []):
            result += f"  - {q}\n"
        if criteria["interview"].get("red_flags_to_rule_out"):
            result += "  Red flags to rule out: " + ", ".join(criteria["interview"]["red_flags_to_rule_out"]) + "\n"

    if "assessment" in criteria:
        result += "\nAssessment - appropriate tests:\n"
        for t in criteria["assessment"].get("appropriate_tests", []):
            result += f"  - {t}\n"

    if "treatment" in criteria:
        result += "\nTreatment - appropriate goals should address:\n"
        for g in criteria["treatment"].get("appropriate_goals", []):
            result += f"  - {g}\n"

    if "home_care" in criteria:
        result += "\nHome Care - appropriate exercises:\n"
        for e in criteria["home_care"].get("appropriate_exercises", []):
            result += f"  - {e}\n"
        if criteria["home_care"].get("important_cautions"):
            result += "  Key cautions: " + ", ".join(criteria["home_care"]["important_cautions"]) + "\n"

    return result


def get_evaluation():
    try:
        client = get_client()

        # Build student submission data with case-specific criteria
        eval_data = f"""Student submission for: {st.session_state.selected_case['name']}

INTERVIEW:
{format_messages_for_eval()}

ASSESSMENTS:
{format_assessments_for_eval()}

TREATMENT GOALS:
{format_treatment_goals_for_eval()}

HOME CARE:
{format_home_care_for_eval()}

ONGOING PLAN:
{format_ongoing_plan_for_eval()}
{format_feedback_criteria()}
"""

        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            system=FEEDBACK_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": eval_data}]
        )
        return response.content[0].text
    except Exception as e:
        st.error(f"Error getting evaluation: {str(e)}")
        return None


def format_messages_for_eval():
    if not st.session_state.messages:
        return "No interview conducted."
    result = ""
    for msg in st.session_state.messages:
        role = "Student" if msg["role"] == "user" else "Patient"
        result += f"{role}: {msg['content']}\n"
    return result


def format_assessments_for_eval():
    if not st.session_state.assessments:
        return "No assessments performed."
    result = ""
    for i, a in enumerate(st.session_state.assessments, 1):
        result += f"{i}. {a['test']} ({a.get('category', 'Unknown')})\n"
        result += f"   Technique: {a['technique']}\n"
        if "movements" in a:
            result += "   Results:\n"
            for movement, data in a["movements"].items():
                status = "Normal" if data.get("normal", True) else "Abnormal"
                result += f"   - {movement}: {data['result']} [{status}]\n"
        else:
            result += f"   Result: {a.get('result', 'N/A')}\n"
        result += "\n"
    return result


def format_treatment_goals_for_eval():
    if not st.session_state.treatment_goals:
        return "No treatment goals set."
    result = ""
    for i, g in enumerate(st.session_state.treatment_goals, 1):
        result += f"{i}. Objective: {g['objective']}\n   Technique: {g['technique']}\n   Tissue: {g['tissue']}\n"
    return result


def format_home_care_for_eval():
    if not st.session_state.home_care:
        return "No home care prescribed."
    result = ""
    for i, h in enumerate(st.session_state.home_care, 1):
        result += f"{i}. Type: {h['type']}\n   Exercise: {h['exercise']}\n   Rationale: {h['rationale']}\n   Benefits: {h['benefits']}\n   Cautions: {h['cautions']}\n   FID: {h['frequency']}, {h['intensity']}, {h['duration']}\n"
    return result


def format_ongoing_plan_for_eval():
    op = st.session_state.ongoing_plan
    if not op:
        return "No ongoing plan provided."
    return f"Follow-up: {op.get('follow_up', 'Not specified')}\nFuture Goals: {op.get('future_goals', 'Not specified')}\nFuture Techniques: {op.get('future_techniques', 'Not specified')}"


def reset_session():
    st.session_state.stage = "case_selection"
    st.session_state.selected_case = None
    st.session_state.messages = []
    st.session_state.assessments = []
    st.session_state.treatment_goals = []
    st.session_state.home_care = []
    st.session_state.ongoing_plan = {}
    st.session_state.feedback = ""
    st.session_state.pending_response = False
    st.session_state.confirm_leave_interview = False


# ============ STAGE VIEWS ============

def show_case_selection():
    st.title("Virtual Patient Training")
    st.markdown("""
    ### Welcome!

    Practice your clinical reasoning skills by working through a complete patient case:
    1. Interview the patient
    2. Perform assessments
    3. Create treatment goals
    4. Prescribe home care
    5. Develop an ongoing plan
    6. Receive feedback

    Select a case to begin.
    """)

    st.divider()

    for case in CASES:
        with st.container():
            if st.button(f"{case['name']} - {case['summary']}", key=case['id'], type="primary"):
                st.session_state.selected_case = case
                st.session_state.stage = "intake"
                st.rerun()


def show_intake():
    case = st.session_state.selected_case
    intake = case.get("intake", {})

    st.title("Patient Intake Form")
    st.caption("Review this information before beginning your interview.")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Patient Name:**")
        st.markdown("**Age:**")
        st.markdown("**Gender:**")
        st.markdown("**Date of Onset:**")
    with col2:
        st.markdown(intake.get("name", "N/A"))
        st.markdown(str(intake.get("age", "N/A")))
        st.markdown(intake.get("gender", "N/A"))
        st.markdown(intake.get("date_of_onset", "N/A"))

    st.divider()

    st.markdown("**Chief Complaint:**")
    st.info(intake.get("chief_complaint", "N/A"))

    st.markdown("**Referral Source:**")
    st.write(intake.get("referral_source", "N/A"))
    if intake.get("referred_by") and intake.get("referred_by") != "N/A":
        st.write(f"Referred by: {intake.get('referred_by')}")

    if intake.get("notes"):
        st.markdown("**Intake Notes:**")
        st.write(intake.get("notes"))

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Case Selection"):
            st.session_state.stage = "case_selection"
            st.session_state.selected_case = None
            st.rerun()
    with col2:
        if st.button("Begin Interview", type="primary"):
            st.session_state.stage = "interview"
            st.rerun()


def show_interview():
    case = st.session_state.selected_case
    st.title("Patient Interview")
    st.caption(f"You are interviewing: {case['name']}")

    # Initialize pending message state
    if "pending_response" not in st.session_state:
        st.session_state.pending_response = False

    # Display chat history
    for msg in st.session_state.messages:
        role_label = "Student" if msg["role"] == "user" else "Patient"
        avatar = "🧑‍🎓" if msg["role"] == "user" else case["avatar"]
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(f"**{role_label}:** {msg['content']}")

    # Show pending user message and generate response
    if st.session_state.pending_response:
        # Show patient thinking indicator
        with st.chat_message("assistant", avatar=case["avatar"]):
            with st.spinner("Patient is thinking..."):
                response = get_patient_response(st.session_state.messages)
                if response:
                    st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.pending_response = False
        st.rerun()

    # Chat input
    if prompt := st.chat_input("Type your question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.pending_response = True
        st.rerun()

    # Navigation with confirmation
    st.divider()
    if "confirm_leave_interview" not in st.session_state:
        st.session_state.confirm_leave_interview = False

    if not st.session_state.confirm_leave_interview:
        if st.button("Continue to Assessments", type="secondary"):
            if len(st.session_state.messages) > 0:
                st.session_state.confirm_leave_interview = True
                st.rerun()
            else:
                st.warning("Please conduct at least one exchange before continuing.")
    else:
        st.warning("Are you sure you want to move on? You cannot return to the interview.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, continue", type="primary"):
                st.session_state.confirm_leave_interview = False
                st.session_state.stage = "assessment"
                st.rerun()
        with col2:
            if st.button("Cancel"):
                st.session_state.confirm_leave_interview = False
                st.rerun()


def get_all_assessments(case):
    """Flatten all assessments into a list with category info."""
    assessments = case.get("assessments", {})
    all_tests = []
    for category, tests in assessments.items():
        for test in tests:
            all_tests.append({"category": category, **test})
    return all_tests


def get_assessment_by_name(case, name):
    """Find assessment by name."""
    for test in get_all_assessments(case):
        if test["name"] == name:
            return test
    return None


def show_assessment():
    case = st.session_state.selected_case
    st.title("Assessments")
    st.caption("Select 2 assessments to perform. For each, describe how you would perform the technique.")

    # Show already added assessments
    if st.session_state.assessments:
        st.subheader("Completed Assessments")
        for i, a in enumerate(st.session_state.assessments):
            with st.expander(f"{i+1}. {a['test']}", expanded=False):
                st.write(f"**Your technique:** {a['technique']}")
                st.divider()
                # Check if this is a ROM test with movements
                if "movements" in a:
                    st.write("**Results by Movement:**")
                    for movement, data in a["movements"].items():
                        status = "✓" if data.get("normal", True) else "⚠️"
                        st.write(f"{status} **{movement}:** {data['result']}")
                else:
                    st.write(f"**Result:** {a['result']}")

    # Add new assessment if less than 2
    if len(st.session_state.assessments) < 2:
        assessment_num = len(st.session_state.assessments) + 1
        st.subheader(f"Assessment {assessment_num}")

        # Get available tests (not already performed)
        completed_names = [a["test"] for a in st.session_state.assessments]
        all_tests = get_all_assessments(case)
        available_tests = [t for t in all_tests if t["name"] not in completed_names]

        # Group by category for selection
        categories = {}
        for test in available_tests:
            cat = test["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(test["name"])

        # Category selection - use dynamic key to reset on submission
        selected_category = st.selectbox(
            "Assessment Category:",
            list(categories.keys()),
            key=f"assessment_category_{assessment_num}"
        )

        # Test selection within category - use dynamic key
        selected_test_name = st.selectbox(
            "Select assessment:",
            categories.get(selected_category, []),
            key=f"assessment_select_{assessment_num}"
        )

        # Get test details
        selected_test = get_assessment_by_name(case, selected_test_name)

        if selected_test:
            # Show description for special tests
            if selected_test["category"] == "Special Tests" and "description" in selected_test:
                st.info(f"**Test description:** {selected_test['description']}")

            # Category-specific inputs
            if selected_test["category"] == "Special Tests":
                positive_outcome = st.text_area(
                    "Describe what a positive outcome would be:",
                    key=f"assessment_positive_{assessment_num}"
                )
                expectation = st.text_area(
                    "Would you expect this test to be positive or negative and why?",
                    key=f"assessment_expectation_{assessment_num}"
                )
                technique = f"Positive outcome: {positive_outcome}\nExpectation: {expectation}"
                inputs_filled = positive_outcome.strip() and expectation.strip()
            elif selected_test["category"] == "ROM":
                affected_rom = st.text_area(
                    "What range of motions do you think would be affected?",
                    key=f"assessment_affected_rom_{assessment_num}"
                )
                technique = affected_rom
                inputs_filled = affected_rom.strip()
            else:
                # Fallback for other categories
                technique = st.text_area(
                    "Describe your assessment approach:",
                    key=f"assessment_technique_{assessment_num}"
                )
                inputs_filled = technique.strip()

            if st.button("Submit Assessment"):
                if inputs_filled:
                    with st.spinner("Performing assessment..."):
                        # Build result based on test type
                        if selected_test["category"] == "ROM":
                            # ROM test - return movements breakdown
                            result_data = {
                                "test": selected_test_name,
                                "category": "ROM",
                                "type": selected_test.get("type", ""),
                                "joint": selected_test.get("joint", ""),
                                "technique": technique,
                                "movements": selected_test["movements"]
                            }
                        else:
                            # Special test or other - return single result
                            result_data = {
                                "test": selected_test_name,
                                "category": selected_test["category"],
                                "technique": technique,
                                "result": selected_test["result"]
                            }

                        st.session_state.assessments.append(result_data)
                    st.rerun()
                else:
                    st.warning("Please fill in all fields.")

    # Navigation
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Interview"):
            st.session_state.stage = "interview"
            st.rerun()
    with col2:
        if st.button("Continue to Treatment Planning", type="primary"):
            if len(st.session_state.assessments) >= 2:
                st.session_state.stage = "treatment_planning"
                st.rerun()
            else:
                st.warning("Please complete 2 assessments before continuing.")


def show_treatment_planning():
    st.title("Treatment Planning")

    goals_remaining = 3 - len(st.session_state.treatment_goals)
    if goals_remaining > 0:
        st.info(f"Create {goals_remaining} more goal{'s' if goals_remaining > 1 else ''} to continue. (3 required)")
    else:
        st.success("All 3 goals created. You can continue to Home Care.")

    # Show already added goals
    if st.session_state.treatment_goals:
        st.subheader("Treatment Goals")
        for i, g in enumerate(st.session_state.treatment_goals):
            with st.expander(f"Goal {i+1}: {g['objective'][:50]}...", expanded=False):
                st.write(f"**Objective:** {g['objective']}")
                st.write(f"**Technique:** {g['technique']}")
                st.write(f"**Target Tissue:** {g['tissue']}")

    # Add new goal if less than 3
    if len(st.session_state.treatment_goals) < 3:
        goal_num = len(st.session_state.treatment_goals) + 1
        st.subheader(f"Goal {goal_num}")

        # Use dynamic keys based on goal count to reset inputs after adding
        objective = st.text_input("Objective (desired outcome):", key=f"goal_objective_{goal_num}")
        technique = st.text_input("Technique to achieve it:", key=f"goal_technique_{goal_num}")
        tissue = st.text_input("Target tissue:", key=f"goal_tissue_{goal_num}")

        if st.button("Add Goal"):
            if objective.strip() and technique.strip() and tissue.strip():
                st.session_state.treatment_goals.append({
                    "objective": objective,
                    "technique": technique,
                    "tissue": tissue
                })
                st.rerun()
            else:
                st.warning("Please fill in all fields.")

    # Navigation
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Assessments"):
            st.session_state.stage = "assessment"
            st.rerun()
    with col2:
        if st.button("Continue to Home Care", type="primary", disabled=(goals_remaining > 0)):
            st.session_state.stage = "home_care"
            st.rerun()


def show_home_care():
    st.title("Home Care")
    st.caption("Prescribe 2 home care exercises. Choose from: Stretch, Strengthen, ADL Change, or Hydrotherapy.")

    home_care_types = ["Stretch", "Strengthen", "ADL Change", "Hydrotherapy"]

    # Show already added home care
    if st.session_state.home_care:
        st.subheader("Prescribed Home Care")
        for i, h in enumerate(st.session_state.home_care):
            with st.expander(f"{i+1}. {h['type']}: {h['exercise']}", expanded=False):
                st.write(f"**Rationale:** {h['rationale']}")
                st.write(f"**Benefits:** {h['benefits']}")
                st.write(f"**Cautions:** {h['cautions']}")
                st.write(f"**Frequency:** {h['frequency']}")
                st.write(f"**Intensity:** {h['intensity']}")
                st.write(f"**Duration:** {h['duration']}")

    # Add new home care if less than 2
    if len(st.session_state.home_care) < 2:
        hc_num = len(st.session_state.home_care) + 1
        st.subheader(f"Home Care {hc_num}")

        # Use dynamic keys to reset inputs after adding
        hc_type = st.selectbox("Type:", home_care_types, key=f"hc_type_{hc_num}")
        exercise = st.text_input("Exercise/Activity:", key=f"hc_exercise_{hc_num}")
        rationale = st.text_area("Rationale:", key=f"hc_rationale_{hc_num}")
        benefits = st.text_area("Benefits:", key=f"hc_benefits_{hc_num}")
        cautions = st.text_area("Cautions:", key=f"hc_cautions_{hc_num}")

        st.markdown("**FID (Frequency, Intensity, Duration):**")
        col1, col2, col3 = st.columns(3)
        with col1:
            frequency = st.text_input("Frequency:", key=f"hc_frequency_{hc_num}")
        with col2:
            intensity = st.text_input("Intensity:", key=f"hc_intensity_{hc_num}")
        with col3:
            duration = st.text_input("Duration:", key=f"hc_duration_{hc_num}")

        if st.button("Add Home Care"):
            if all([exercise.strip(), rationale.strip(), benefits.strip(), cautions.strip(),
                    frequency.strip(), intensity.strip(), duration.strip()]):
                st.session_state.home_care.append({
                    "type": hc_type,
                    "exercise": exercise,
                    "rationale": rationale,
                    "benefits": benefits,
                    "cautions": cautions,
                    "frequency": frequency,
                    "intensity": intensity,
                    "duration": duration
                })
                st.rerun()
            else:
                st.warning("Please fill in all fields.")

    # Navigation
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Treatment Planning"):
            st.session_state.stage = "treatment_planning"
            st.rerun()
    with col2:
        if st.button("Continue to Ongoing Plan", type="primary"):
            if len(st.session_state.home_care) >= 2:
                st.session_state.stage = "ongoing_plan"
                st.rerun()
            else:
                st.warning("Please prescribe 2 home care exercises before continuing.")


def show_ongoing_plan():
    st.title("Ongoing Plan")
    st.caption("Outline your plan for continued care.")

    follow_up = st.text_input("When would you like to see the patient next?",
                              value=st.session_state.ongoing_plan.get("follow_up", ""),
                              key="op_follow_up")
    future_goals = st.text_area("What are the goals for future treatments?",
                                value=st.session_state.ongoing_plan.get("future_goals", ""),
                                key="op_future_goals")
    future_techniques = st.text_area("What techniques or areas would you focus on in future appointments?",
                                     value=st.session_state.ongoing_plan.get("future_techniques", ""),
                                     key="op_future_techniques")

    # Auto-save ongoing plan
    st.session_state.ongoing_plan = {
        "follow_up": follow_up,
        "future_goals": future_goals,
        "future_techniques": future_techniques
    }

    # Navigation
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Home Care"):
            st.session_state.stage = "home_care"
            st.rerun()
    with col2:
        if st.button("Complete examination and get feedback", type="primary"):
            if all([follow_up.strip(), future_goals.strip(), future_techniques.strip()]):
                with st.spinner("Generating feedback..."):
                    feedback = get_evaluation()
                    if feedback:
                        st.session_state.feedback = feedback
                        st.session_state.stage = "evaluation"
                        st.rerun()
            else:
                st.warning("Please fill in all fields.")


def show_evaluation():
    st.title("Evaluation & Feedback")

    # Summary of what was done
    with st.expander("View Interview Transcript", expanded=False):
        for msg in st.session_state.messages:
            role_label = "Student" if msg["role"] == "user" else "Patient"
            st.write(f"**{role_label}:** {msg['content']}")

    with st.expander("View Assessments", expanded=False):
        for i, a in enumerate(st.session_state.assessments, 1):
            st.write(f"**{i}. {a['test']}**")
            st.write(f"Technique: {a['technique']}")
            if "movements" in a:
                for movement, data in a["movements"].items():
                    status = "Normal" if data.get("normal", True) else "Abnormal"
                    st.write(f"- {movement}: {data['result']} [{status}]")
            else:
                st.write(f"Result: {a['result']}")
            st.write("---")

    with st.expander("View Treatment Goals", expanded=False):
        for i, g in enumerate(st.session_state.treatment_goals, 1):
            st.write(f"**Goal {i}:** {g['objective']}")
            st.write(f"Technique: {g['technique']}")
            st.write(f"Tissue: {g['tissue']}")
            st.write("---")

    with st.expander("View Home Care", expanded=False):
        for i, h in enumerate(st.session_state.home_care, 1):
            st.write(f"**{i}. {h['type']}: {h['exercise']}**")
            st.write(f"FID: {h['frequency']}, {h['intensity']}, {h['duration']}")
            st.write("---")

    with st.expander("View Ongoing Plan", expanded=False):
        op = st.session_state.ongoing_plan
        st.write(f"**Follow-up:** {op.get('follow_up', 'N/A')}")
        st.write(f"**Future Goals:** {op.get('future_goals', 'N/A')}")
        st.write(f"**Future Techniques:** {op.get('future_techniques', 'N/A')}")

    # Show feedback
    st.divider()
    st.subheader("Feedback")
    st.markdown(st.session_state.feedback)

    # Reset
    st.divider()
    if st.button("Start New Session", type="primary"):
        reset_session()
        st.rerun()


def main():
    st.set_page_config(
        page_title="Virtual Patient Training",
        page_icon="🏥",
        layout="centered"
    )

    init_session_state()

    # Stage routing
    if st.session_state.stage == "case_selection":
        show_case_selection()
    elif st.session_state.stage == "intake":
        show_intake()
    elif st.session_state.stage == "interview":
        show_interview()
    elif st.session_state.stage == "assessment":
        show_assessment()
    elif st.session_state.stage == "treatment_planning":
        show_treatment_planning()
    elif st.session_state.stage == "home_care":
        show_home_care()
    elif st.session_state.stage == "ongoing_plan":
        show_ongoing_plan()
    elif st.session_state.stage == "evaluation":
        show_evaluation()


if __name__ == "__main__":
    main()
