# Tennis Elbow Case - Michael Torres
# Lateral epicondylalgia, chronic presentation

CASE = {
    "id": "tennis_elbow",
    "name": "Michael Torres",
    "summary": "42yo recreational tennis player, lateral elbow pain (chronic)",
    "avatar": "🎾",
    "intake": {
        "name": "Michael Torres",
        "age": 42,
        "gender": "Male",
        "chief_complaint": "Right elbow pain",
        "referral_source": "Self-referred",
        "referred_by": "N/A",
        "date_of_onset": "6 weeks ago",
        "notes": "Patient reports pain with gripping activities and tennis. Family doctor suggested 'tennis elbow'."
    },
    "details": """
Patient Name: Michael Torres
Age: 42
Occupation: Accountant (desk job), plays recreational tennis 2-3x/week
Dominant hand: Right

PRESENTING COMPLAINT: Right lateral elbow pain for 6 weeks

CASE DETAILS:
- Location: Right lateral elbow, specifically around the lateral epicondyle. Pain sometimes radiates into the forearm extensors.
- MOI: Gradual onset. No specific injury. Has been playing more tennis lately (increased from 1x to 3x per week over the past 2 months). Also does a lot of computer mouse work at his accounting job.
- Nature: This is a chronic condition. Dull ache at rest, sharp pain with gripping or wrist extension activities.
- Onset: Started about 6 weeks ago, has gradually worsened.
- Pain: 3/10 at rest, 6-7/10 with gripping activities (opening jars, shaking hands, backhand in tennis). Pain is worse during activity, not just after.
- Quality: Dull, aching at rest. Sharp, burning with gripping or resisted wrist extension.
- Referral: Pain occasionally refers down into the forearm extensor muscles. No numbness or tingling in the hand.
- Systemic: No fever, no night sweats, no unexplained weight loss, generally healthy.
- Timing: Worse during and after tennis. Aggravated by computer mouse use at work. Stiff in the morning for about 10 minutes. Feels better with rest but flares quickly with activity.
- Underlying: No previous elbow problems. No neck issues. Generally healthy, no medications.
- HCP: Saw his family doctor 2 weeks ago who said it was "tennis elbow" and suggested rest and ice. Has not seen a physiotherapist or anyone else.
- Goal: Wants to keep playing tennis without pain. Doesn't want to give up the sport. Also needs to be able to work at computer without discomfort.

PERSONALITY: Motivated and active. A bit frustrated that rest hasn't helped much. Asks good questions about his condition. Wants to understand the "why" behind recommendations.

ASSESSMENT RESULTS:
- Active ROM Elbow: Full range, no pain
- Passive ROM Elbow: Full range, minor discomfort at end-range pronation
- Active ROM Wrist: Full range but poorer quality of movement. Pain with end-range extension.
- Passive ROM Wrist: End-range flexion with ulnar deviation provokes symptoms. Extension with radial deviation also provokes symptoms.
- Resisted ROM Wrist: Extension and radial deviation provoke symptoms
- Cozen's Test (resisted wrist extension and radial deviation): POSITIVE - reproduces lateral elbow pain
- Maudsley's Test (resisted third digit extension): POSITIVE - reproduces lateral elbow pain
- Mill's Test (passive wrist flexion and ulnar deviation with elbow extended): POSITIVE - reproduces lateral elbow pain
- Varus Stress Test: NEGATIVE - no instability
- Grip Strength Test: Reduced grip strength (approximately 8% weaker on right vs left). Notable reduction in grip with elbow fully extended compared to 90 degrees flexion.
- Palpation: Tenderness at lateral epicondyle and ECRB tendon. Trigger points in extensor digitorum and ECU.

CLINICAL IMPRESSION: Consistent with lateral epicondylalgia of moderate severity in the chronic (not acutely flared) state. Primary involvement of ECRB tendon.

APPROPRIATE TREATMENT GOALS:
1. Reduce adhesions around the common extensor tendon (CET) with skin rolling
2. Promote normal resting muscle tone of ECRB using segmental muscle stripping, petrissage, origin-insertion
3. Decrease TrP activity in extensor digitorum with TrP treatment protocol
4. Improve quality of AROM wrist extension with MFR to WAD of 3 and flexors
5. Promote tendon remodelling with petrissage, frictions, or specific compression on CET
6. Promote tendon strength with isometric and eccentric contractions

APPROPRIATE HOME CARE:
- Gentle extensor stretching (wrist flexion with elbow extended, progress to elbow flexed)
- Ice after activity (10-15 minutes)
- Isometric wrist extension exercises (pain should not exceed 5/10, no worse next day)
- Progress to eccentric wrist extension with resistance band (elbow flexed initially, progress to extended)
- Activity modification: adjust grip size on tennis racquet, consider counterforce brace
- Reduce total volume of tennis temporarily, focus on technique (avoid leading with elbow)

EXPECTED OUTCOMES: Nearly all people have complete symptom resolution within 1 year. Recommend weekly treatment until symptom provocation improves (2-8 weeks), then reduce to every 2-6 weeks.

CAUTIONS: If first treatment, treat conservatively. Pain during exercise should not exceed 5/10 and should not be worse the next day.
""",
    "assessments": {
        "ROM": [
            {
                "name": "Active ROM - Elbow",
                "type": "AROM",
                "joint": "Elbow",
                "movements": {
                    "Flexion": {"result": "Full range, no pain", "normal": True},
                    "Extension": {"result": "Full range, no pain", "normal": True},
                    "Pronation": {"result": "Full range, no pain", "normal": True},
                    "Supination": {"result": "Full range, no pain", "normal": True}
                }
            },
            {
                "name": "Passive ROM - Elbow",
                "type": "PROM",
                "joint": "Elbow",
                "movements": {
                    "Flexion": {"result": "Full range, no pain", "normal": True},
                    "Extension": {"result": "Full range, no pain", "normal": True},
                    "Pronation": {"result": "Full range, minor discomfort at end-range", "normal": False},
                    "Supination": {"result": "Full range, no pain", "normal": True}
                }
            },
            {
                "name": "Active ROM - Wrist",
                "type": "AROM",
                "joint": "Wrist",
                "movements": {
                    "Flexion": {"result": "Full range, no pain", "normal": True},
                    "Extension": {"result": "Full range but poorer quality of movement, pain at end-range", "normal": False},
                    "Radial Deviation": {"result": "Full range, mild discomfort", "normal": False},
                    "Ulnar Deviation": {"result": "Full range, no pain", "normal": True}
                }
            },
            {
                "name": "Passive ROM - Wrist",
                "type": "PROM",
                "joint": "Wrist",
                "movements": {
                    "Flexion": {"result": "Full range, no pain", "normal": True},
                    "Extension": {"result": "Full range, pain with radial deviation combined", "normal": False},
                    "Radial Deviation": {"result": "Provokes symptoms when combined with extension", "normal": False},
                    "Ulnar Deviation": {"result": "Provokes symptoms when combined with flexion", "normal": False}
                }
            },
            {
                "name": "Resisted ROM - Wrist",
                "type": "RROM",
                "joint": "Wrist",
                "movements": {
                    "Flexion": {"result": "Strong, no pain", "normal": True},
                    "Extension": {"result": "Provokes lateral elbow pain", "normal": False},
                    "Radial Deviation": {"result": "Provokes lateral elbow pain", "normal": False},
                    "Ulnar Deviation": {"result": "Strong, no pain", "normal": True}
                }
            }
        ],
        "Special Tests": [
            {
                "name": "Cozen's Test",
                "description": "Resisted wrist extension and radial deviation with elbow extended",
                "result": "POSITIVE - reproduces lateral elbow pain",
                "positive": True
            },
            {
                "name": "Maudsley's Test",
                "description": "Resisted third digit (middle finger) extension",
                "result": "POSITIVE - reproduces lateral elbow pain",
                "positive": True
            },
            {
                "name": "Mill's Test",
                "description": "Passive wrist flexion and ulnar deviation with elbow extended",
                "result": "POSITIVE - reproduces lateral elbow pain",
                "positive": True
            },
            {
                "name": "Varus Stress Test",
                "description": "Lateral stability test of the elbow",
                "result": "NEGATIVE - no instability noted",
                "positive": False
            }
        ],
        "Other": [
            {
                "name": "Grip Strength Test",
                "description": "Compare grip strength bilaterally, test at 0 and 90 elbow flexion",
                "result": "Reduced grip strength (approximately 8% weaker on right vs left). Notable reduction in grip with elbow fully extended compared to 90 flexion."
            },
            {
                "name": "Palpation - Lateral Elbow",
                "description": "Palpate lateral epicondyle, common extensor tendon, and surrounding muscles",
                "result": "Tenderness at lateral epicondyle and ECRB tendon. Trigger points noted in extensor digitorum and ECU."
            }
        ]
    },
    "feedback_criteria": {
        "condition_name": "lateral epicondylalgia (tennis elbow)",
        "interview": {
            "key_questions": [
                "Location of pain (lateral elbow, lateral epicondyle)",
                "Aggravating activities (gripping, tennis backhand, mouse use)",
                "Pain rating and when it occurs",
                "Onset and duration (6 weeks, gradual)",
                "Previous treatment (saw family doctor, rest/ice)",
                "Patient goals (continue tennis, work without pain)"
            ],
            "red_flags_to_rule_out": [
                "Numbness/tingling (neural involvement)",
                "Neck pain (cervical referral)",
                "Systemic symptoms"
            ]
        },
        "assessment": {
            "appropriate_tests": [
                "Resisted wrist extension tests (Cozen's, Maudsley's)",
                "Mill's Test (passive stretch)",
                "Grip strength comparison",
                "Palpation of lateral epicondyle/ECRB"
            ],
            "key_findings": [
                "Positive Cozen's/Maudsley's/Mill's tests",
                "Pain with resisted wrist extension",
                "Tenderness at lateral epicondyle",
                "Reduced grip strength with elbow extended"
            ]
        },
        "treatment": {
            "appropriate_goals": [
                "Address ECRB/common extensor tendon",
                "Reduce trigger points in forearm extensors",
                "Improve wrist extension quality",
                "Promote tendon healing/remodelling"
            ],
            "appropriate_techniques": [
                "Soft tissue work to extensors",
                "Frictions to tendon",
                "Trigger point treatment",
                "MFR to forearm"
            ]
        },
        "home_care": {
            "appropriate_exercises": [
                "Wrist extensor stretching",
                "Isometric wrist extension (progress to eccentric)",
                "Ice after activity"
            ],
            "important_cautions": [
                "Pain during exercise should not exceed 5/10",
                "Should not be worse the next day",
                "Activity modification (grip size, technique)"
            ]
        }
    }
}
