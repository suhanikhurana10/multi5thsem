
import spacy
import re

# Load Spacy
try:
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = None

# =========================================================
# DOMAIN DICTIONARIES
# =========================================================

MATH_TERMS = {
    "evaluate": "solve",
    "compute": "find",
    "calculate": "find",
    "determine": "find",
    "derive": "get",
    "integrate": "find the area total",
    "differentiate": "find the rate of change",
    "summation": "total",
    "product": "multiplication result",
    "quotient": "division result",
    "remainder": "leftover",
    "equivalent": "equal",
    "approximately": "about",
    "magnitude": "size",
    "vector": "arrow with direction",
    "variable": "unknown letter",
    "coefficient": "number part",
    "polynomial": "math expression",
    "perpendicular": "at 90 degrees",
    "parallel": "side by side",
    "vertex": "corner",
    "hypotenuse": "long side",
    "circumference": "perimeter",
    "radius": "distance to center",
    "diameter": "width across center",
    "function": "rule",
    "domain": "inputs",
    "range": "outputs"
}

PHYSICS_TERMS = {
    "velocity": "speed",
    "acceleration": "change in speed",
    "momentum": "movement power",
    "friction": "rubbing resistance",
    "gravity": "downward pull",
    "force": "push or pull",
    "exert": "apply",
    "magnitude": "strength",
    "displacement": "distance moved",
    "trajectory": "path",
    "projectile": "flying object",
    "equilibrium": "balance",
    "kinetic": "moving",
    "potential": "stored",
    "thermal": "heat",
    "dissipate": "scatter",
    "conservation": "saving",
    "collision": "crash",
    "optics": "light behavior",
    "thermodynamics": "heat study",
    "quantum": "smallest particle study"
}

BIOLOGY_TERMS = {
    "mitochondria": "energy maker",
    "nucleus": "control center",
    "photosynthesis": "sunlight to food process",
    "respiration": "breathing",
    "evolution": "change over time",
    "hypothesis": "guess",
    "organism": "living thing",
    "cellular": "cell-based",
    "metabolism": "energy use",
    "taxonomy": "naming system",
    "ecosystem": "living environment",
    "biodiversity": "variety of life",
    "genetics": "trait study",
    "heredity": "passed-down traits",
    "mutation": "genetic change"
}

CHEMISTRY_TERMS = {
    "molecule": "group of atoms",
    "stoichiometry": "mass balance calculation",
    "catalyst": "speed-upper",
    "reaction": "change",
    "solubility": "dissolving ability",
    "viscosity": "thickness",
    "isotope": "atom variant",
    "oxidation": "reaction with oxygen",
    "reduction": "gaining electrons",
    "covalent": "shared electron",
    "ionic": "stolen electron",
    "equilibrium": "balance",
    "precipitate": "solid formed",
    "concentration": "strength"
}


GENERAL_ACADEMIC = {
    "demonstrate": "show",
    "illustrate": "show",
    "depict": "show",
    "utilize": "use",
    "employ": "use",
    "leverage": "use",
    "examine": "look at",
    "investigate": "check",
    "analyze": "study",
    "facilitate": "help",
    "ameliorate": "improve",
    "commence": "start",
    "terminate": "end",
    "cease": "stop",
    "regarding": "about",
    "concerning": "about",
    "pertaining to": "about",
    "furthermore": "also",
    "moreover": "also",
    "nevertheless": "however",
    "consequently": "so",
    "therefore": "so",
    "thus": "so",
    "appropriate": "right",
    "erroneous": "wrong",
    "fundamental": "key",
    "significant": "big",
    "substantial": "big",
    "considerable": "big",
    "minimal": "small",
    "optimal": "best",
    "objective": "goal",
    "strategy": "plan",
    "implement": "do",
    "execute": "do",
    "accomplish": "do",
    "achieve": "get",
    "acquire": "get",
    "obtain": "get",
    "modify": "change",
    "alter": "change",
    "transform": "change",
    "reside": "live"
}

LOGIC_TERMS = {
    "consequently": "so",
    "subsequently": "later",
    "furthermore": "also",
    "nevertheless": "but",
    "conversely": "opposite",
    "regarding": "about",
    "hypothesis": "guess",
    "assumption": "belief",
    "criterion": "rule",
    "validity": "truth",
    "premise": "basis",
    "deduction": "conclusion",
    "induction": "generalization",
    "correlation": "link",
    "causation": "cause"
}

# NEW: Hallucination & Speculation Prevention
# Terms that should NEVER be introduced or treated as fact
BLOCKED_TERMS = {
    "antigravity", "perpetual motion", "cold fusion", "warp drive",
    "telepathy", "telekinesis", "force field", "aether", "phlogiston",
    "creationism", "flat earth", "alchemy"
}

# NEW: Expanded Scientific Vocabulary (Educational Enhancement)
ADVANCED_SCIENCE = {
    "quantum entanglement": "linked particles",
    "superposition": "state combination",
    "relativity": "physics of speed and gravity",
    "thermodynamics": "heat study",
    "entropy": "disorder",
    "enthalpy": "heat energy",
    "homeostasis": "balance",
    "symbiosis": "living together",
    "osmosis": "water movement",
    "mitosis": "cell division",
    "meiosis": "reproduction cell division",
    "enzyme": "reaction helper",
    "pathogen": "germ",
    "antibody": "germ fighter",
    "neuron": "nerve cell",
    "synapse": "nerve connection",
    "plate tectonics": "earth crust movement",
    "photosynthesis": "sunlight energy process",
    "respiration": "energy release"
}



# Combine all into one master map
MASTER_MAP = {
    **MATH_TERMS, 
    **PHYSICS_TERMS, 
    **GENERAL_ACADEMIC,
    **BIOLOGY_TERMS,
    **CHEMISTRY_TERMS,
    **LOGIC_TERMS,
    **ADVANCED_SCIENCE
}



# Difficult Terms that need explanation (in brackets) instead of direct replacement
EXPLANATION_MAP = {
    "mitochondria": " (the cell's power plant)",
    "photosynthesis": " (process of using light to make food)",
    "stoichiometry": " (calculation of reactants and products)",
    "derivative": " (instantaneous rate of change)",
    "integral": " (area under the curve)",
    "quantum": " (relating to the smallest scale of energy)",
    "relativity": " (physics of high speed and gravity)"
}



# Phrases to remove or shorten
FLUFF_REMOVAL = {
    r"it is important to note that": "",
    r"bear in mind that": "remember",
    r"in order to": "to",
    r"due to the fact that": "because",
    r"in the event that": "if",
    r"at this point in time": "now",
    r"until such time as": "until",
    r"with the exception of": "except",
    r"for the purpose of": "to",
    r"make an attempt": "try",
    r"give consideration to": "consider",
    r"is capable of": "can"
}


def simplify_vocabulary(text):
    """Replaces complex words with simple ones using Spacy for context/lemmatization if needed (basic string replacement for now for speed)."""
    doc = nlp(text) if nlp else None
    words_out = []
    
    if not doc:
        return text # fallback

    for token in doc:
        word = token.text
        lower_word = word.lower()
        
        # Check lemma?
        lemma = token.lemma_.lower()
        
        replacement = None
        
        if lower_word in MASTER_MAP:
            replacement = MASTER_MAP[lower_word]
            # SAFETY CHECK: Do not introduce blocked terms
            if any(b in replacement.lower() for b in BLOCKED_TERMS):
                replacement = None 
        elif lemma in MASTER_MAP:

            replacement = MASTER_MAP[lemma]
            
        # Check for explanation necessity
        explanation = ""
        if lower_word in EXPLANATION_MAP:
            explanation = EXPLANATION_MAP[lower_word]
        elif lemma in EXPLANATION_MAP:
            explanation = EXPLANATION_MAP[lemma]

        if replacement:
            # Preserve capitalization
            if word.istitle():
                replacement = replacement.capitalize()
            words_out.append(replacement + explanation)
        else:
            # Preserve whitespace
            # If no replacement but needs explanation
            if explanation:
                 words_out.append(token.text + explanation + token.whitespace_)
            else:
                 words_out.append(token.text_with_ws)
            
    return "".join(words_out)


def remove_fluff(text):
    """Removes verbose academic phrasing"""
    for phrase, replacement in FLUFF_REMOVAL.items():
        text = re.sub(phrase, replacement, text, flags=re.IGNORECASE)
    return text

def split_long_sentences(text):
    """Splits sentences based on common conjunctions/punctuation if they are too long."""
    # This is a heuristic. 
    # Valid splitting tokens: ";", "whereas", "while" (sometimes), ". However,"
    
    # 1. Replace semi-colons with periods
    text = text.replace(";", ".")
    
    # 2. Split complex clauses
    # "Because X, Y" -> "X. So Y."
    # Case insensitive
    text = re.sub(r'Because (.*?), (.*)', r'\1. So \2', text, flags=re.IGNORECASE)
    text = re.sub(r'Although (.*?), (.*)', r'\1. But \2', text, flags=re.IGNORECASE)
    text = re.sub(r'(.*), whereas (.*)', r'\1. But \2', text, flags=re.IGNORECASE)
    
    return text


def simplify_text(text, aggression=2):
    """
    simplify_text with adaptive aggression.
    aggression (int):
      1: Minimal (Fluff removal only)
      2: Standard (Fluff + Vocabulary)
      3: Aggressive (Fluff + Vocabulary + Sentence Splitting)
    """
    if not text: return ""
    
    # 1. Structural cleanup (Fluff removal is always safe/good)
    text = remove_fluff(text)
    
    # Aggression 3: Split long sentences
    if aggression >= 3:
        text = split_long_sentences(text)
    
    # Aggression 2+: Vocabulary Substitution
    if aggression >= 2:
        # Running it via Spacy to handle tokenization nicely
        if nlp:
            text = simplify_vocabulary(text)
        else:
            # Fallback simple replace if spacy fails
            for key, val in MASTER_MAP.items():
                 text = re.sub(r'\b' + re.escape(key) + r'\b', val, text, flags=re.IGNORECASE)

    # 3. Final cleanup
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 4. SAFETY GUARANTEE (Anti-Hallucination)
    # Strictly remove blocked terms even if they came from input
    for blocked in BLOCKED_TERMS:
        pattern = r'\b' + re.escape(blocked) + r'\b'
        if re.search(pattern, text, flags=re.IGNORECASE):
             text = re.sub(pattern, "[Unsupported Concept]", text, flags=re.IGNORECASE)

    return text


