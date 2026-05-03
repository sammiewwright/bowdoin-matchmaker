from user_profile import Profile

class Matcher:
    def __init__(self, profiles):
        self.profiles = profiles 
        
    def count_matches(self, matches, index=0):
        if index >= len(matches):
            return 0
        return 1 + self.count_matches(matches, index + 1)
    
    def gender_compatible(self, p1, p2):
        # If either person is looking for friendship, allow any gender
        if p1.goal == "friend" and p2.goal == "friend":
            return True

        # For casual/relationship, both people's preferences must accept the other's gender
        p1_accepts_p2 = (p1.preferred_gender == "Any" or p1.preferred_gender == p2.gender)
        p2_accepts_p1 = (p2.preferred_gender == "Any" or p2.preferred_gender == p1.gender)

        return p1_accepts_p2 and p2_accepts_p1

    def calculate_score(self, p1, p2):
        score = 0

        # reject incompatible gender preferences for non-friend matches
        if not self.gender_compatible(p1, p2):
            return 0
        
        # same goal
        if p1.goal == p2.goal:
            score += 3

        # shared interests
        shared = p1.get_interests().intersection(p2.get_interests())
        score += len(shared) * 2

        # same music
        if p1.music_type == p2.music_type:
            score += 1

        # age difference
        if abs(p1.age - p2.age) <= 2:
            score += 2

        return score

    def find_matches(self, target, min_score = 4):
        matches = []

        for profile in self.profiles:
            if profile != target:
                score = self.calculate_score(target, profile)
                if score >= min_score:
                    matches.append((profile, score))  

        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:3]
    
    
