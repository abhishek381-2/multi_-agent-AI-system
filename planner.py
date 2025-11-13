import datetime

def create_revision_plan(topics_list):
    """
    Topics ki list ke aadhaar par ek simple revision plan banata hai.
    """
    plan = []
    today = datetime.date.today()
    
    # Har topic ko 2 din ke gap par revise karne ka plan
    for i, topic in enumerate(topics_list):
        revise_date = today + datetime.timedelta(days=(i + 1) * 2)
        plan.append({
            "topic": topic,
            "revise_on": str(revise_date),
            "status": "Pending"
        })
    return plan