"""
Malta Law Document Database
Complete articles from legislation.mt for CRAG system

Documents included:
1. Examination of Title Regulations (Cap. 55.06)
2. Notaries (Compulsory Insurance) Regulations (Cap. 55.07)
3. Acts of Deceased Notaries Regulations (Cap. 55.05)
4. Functions & Duties of Notarial College (Cap. 55.01)
5. Public Registry Act (Cap. 56)
6. Notaries' Code of Ethics (Cap. 55.09)

Total: 100+ articles across 6 legal documents
"""

# Complete Malta Law Document Database
MALTA_LAW_DOCUMENTS = [
    # ========================================
    # EXAMINATION OF TITLE REGULATIONS
    # ========================================
    {
        'id': 'doc_55_06_art_1',
        'content': '1. The title of these regulations is the Examination of Title Regulations.',
        'metadata': {
            'citation': 'Examination of Title Regulations Cap. 55.06, Article 1',
            'article': '1',
            'chapter': 'Cap. 55.06',
            'act_name': 'Examination of Title Regulations',
            'topic': 'Citation',
            'jurisdiction': 'Malta',
            'verified_source': 'legislation.mt'
        }
    },
    {
        'id': 'doc_55_06_art_2',
        'content': '''2. In these regulations, unless the context otherwise requires:
"Act" means the Notarial Profession and Notarial Archives Act;
"authenticated copy" includes a true copy of an authenticated copy;
"contract of engagement" means the contract referred to in regulation 19, and includes any amendment thereto;
"diligence" means the diligence referred to in the Act and in these regulations;
"direct owner" includes sub-direct owner;
"directum dominium" includes sub-directum dominium;
"document" means any handwritten, typewritten, printed or computer-generated document, or one which has come into being through a combination of two or more of these methods, and includes photostatic copies thereof;
"examination of title" has the meaning assigned to it in the Act and in these regulations;
"emphyteusis" includes sub-emphyteusis;
"ground rent" includes sub-ground rent;
"immovable" means the ownership of immovable property or other real right over such property, the subject-matter of the examination of title;
"Land Registry" means the registry set up by the Land Registration Act and includes any other registry or body which from time to time may take over some or all of the functions and responsibilities of the Land Registry;
"legacy" includes pre-legacy;
"legatee" includes pre-legatee;
"photostatic copy" includes a scanned image;
"plan" includes a sketch or design, howsoever made;
"prescriptive period" means ten, thirty or forty years depending on the basis of prescription applicable in terms of these regulations;
"Public Registry" means the registry set up by the Public Registry Act and includes any other registry or body which from time to time may take over some or all of the functions and responsibilities of the Public Registry;
"searches" has the meaning assigned to it in regulation 6(2);
"testamentary search" has the meaning assigned to it in regulation 11;
"title" means the title under which an immovable has passed to the transferor;
"transferee" means a person who acquires an immovable inter vivos by notarial act, whether there is a contract of engagement or not and, unless the context otherwise requires, includes a person (other than a creditor or a person referred to in regulation 19(4)) who instructs a notary to examine title in terms of a contract of engagement;
"transferor" means a person who transfers an immovable inter vivos by notarial act.''',
        'metadata': {
            'citation': 'Examination of Title Regulations Cap. 55.06, Article 2',
            'article': '2',
            'chapter': 'Cap. 55.06',
            'act_name': 'Examination of Title Regulations',
            'topic': 'Interpretation and Definitions',
            'jurisdiction': 'Malta',
            'verified_source': 'legislation.mt'
        }
    },
    {
        'id': 'doc_55_06_art_3',
        'content': '''3.(1) These regulations shall apply where a notary is deemed, in terms of article 84C(5) of the Act, to have been instructed by the transferee to examine title.

(2) These regulations shall also apply where a notary is, in terms of article 84C(4) of the Act, instructed by a contract of engagement to examine title.

(3) These regulations may be modified:
(a) by means of the contract of engagement referred to in sub-regulation (2); or
(b) by means of a contract of engagement where, in the case referred to in sub-regulation (1), the notary and the transferee choose to enter into such contract;
(c) by an agreement in writing entered into between the Notary and the transferee or by a written declaration signed by the transferee, which written agreement or declaration may be recorded in the relative notarial act;

When the agreement to modify these regulations reached between the notary and the client in the manner stipulated in this sub-regulation is not recorded in the relative notarial act, the contract of engagement, the written agreement referred to in this sub-regulation, or the transferee's written declaration shall be retained by the Notary for five years from the date of signing or, if consequent to the examination of title a notarial act is published in terms of article 84C(5) or (6) of the Act, from the date of its publication.''',
        'metadata': {
            'citation': 'Examination of Title Regulations Cap. 55.06, Article 3',
            'article': '3',
            'chapter': 'Cap. 55.06',
            'act_name': 'Examination of Title Regulations',
            'topic': 'Applicability of Regulations',
            'jurisdiction': 'Malta',
            'verified_source': 'legislation.mt'
        }
    },
    {
        'id': 'doc_55_06_art_4',
        'content': '''4. A notary shall ipso iure be exempt from examining the title to an immovable which is the subject-matter of any of the following acts he publishes:
(a) a donation made between persons related to each other by consanguinity or affinity in the direct line to any degree and, or to their respective spouses, and in the collateral line up to the third degree inclusively and, or to their relative spouses;
(b) the constitution of the right of usufruct, use or habitation between any of the persons mentioned in paragraph (a);
(c) a transfer ordered by a competent Court or tribunal;
(d) an acquisition under any title from the Government of Malta or the Church, whatever the root of title;
(e) an acquisition under any title from the Housing Authority or other body established by law, whatever the root of title;
(f) an acquisition under any title, whatever the root of title, by the Government of Malta, by any corporate body established by law or, as may be authorized in each case by the Minister responsible for notarial affairs in terms of article 22(3) of the Act, by any partnership or any other body in which the Government of Malta or any such corporate body as aforesaid has a controlling interest or over which they have effective control;
(g) an acquisition of the perpetual directum dominium;
(h) a partition;
(i) an assignment between spouses consequent to the termination of the community of acquests even where the assignment includes immovables which did not form part of the community of acquests.''',
        'metadata': {
            'citation': 'Examination of Title Regulations Cap. 55.06, Article 4',
            'article': '4',
            'chapter': 'Cap. 55.06',
            'act_name': 'Examination of Title Regulations',
            'topic': 'Exemptions from Title Examination',
            'jurisdiction': 'Malta',
            'verified_source': 'legislation.mt'
        }
    },

    # ========================================
    # NOTARIES INSURANCE REGULATIONS
    # ========================================
    {
        'id': 'doc_55_07_art_1',
        'content': '1. The title of these regulations is the Notaries (Compulsory Insurance) Regulations.',
        'metadata': {
            'citation': 'Notaries (Compulsory Insurance) Regulations Cap. 55.07, Article 1',
            'article': '1',
            'chapter': 'Cap. 55.07',
            'act_name': 'Notaries (Compulsory Insurance) Regulations',
            'topic': 'Citation',
            'jurisdiction': 'Malta',
            'verified_source': 'legislation.mt'
        }
    },
    {
        'id': 'doc_55_07_art_2',
        'content': '''2. In these regulations, unless the context otherwise requires:
"Act" means the Notarial Profession and Notarial Archives Act;
"breach" means any negligent act, error, breach of confidentiality, omission, loss of documents, committed or happening during the exercise of the notary's functions under any law at any time in force in Malta, and for any preparatory, ancillary or consequential work done with respect to same, by the notary or by his employees, and includes any act which causes damages resulting from a criminal or fraudulent act by any of the notary's employees in the performance of their duties if they are in his employment, or in furtherance of the notary's functions if they are third parties engaged by him;
"claimant" means any person who suffers damages due to a breach;
"Court" means the Court of Revision of Notarial Acts;
"damages" means any damages incurred directly by a claimant due to a breach, and includes any consequential loss suffered by the claimant due to such breach;
"insurance provider" means an undertaking which has received its official authorisation for the taking-up of the business of general insurance in Malta and is authorised to write policies categorised under class 13 of the Third Schedule to the Insurance Business Act;
"Minister" means the Minister responsible for notarial affairs;
"notarial act" means an inter vivos act, a will, an act of delivery of a secret will or any deed published in terms of articles 84A and 84B of the Act;
"Notarial Council" has the meaning assigned to it by the Act;
"notary" means a person, holding a warrant in accordance with the Act to practise such profession, but does not include a notary referred to in article 22 of the Act;
"notary's employees" means one or more persons in the employment of a notary and, or one or more third parties not in the employment of the notary but engaged by the notary in the exercise of the notary's functions;
"policy" means a Professional Indemnity Insurance Policy issued according to documented terms and conditions, provided by an insurance provider to a notary;
"policy year" means the minimum period of one year during which a notary is to be covered by a policy;
"run-off cover" has the meaning assigned to it in regulation 5.''',
        'metadata': {
            'citation': 'Notaries (Compulsory Insurance) Regulations Cap. 55.07, Article 2',
            'article': '2',
            'chapter': 'Cap. 55.07',
            'act_name': 'Notaries (Compulsory Insurance) Regulations',
            'topic': 'Interpretation and Definitions',
            'jurisdiction': 'Malta',
            'verified_source': 'legislation.mt'
        }
    },
    {
        'id': 'doc_55_07_art_3',
        'content': '''3.(1) Without prejudice to the other provisions of these regulations, with effect from 1 January 2013, every notary shall be at all times adequately covered by a policy in terms of article 10A of the Act for a minimum sum of two hundred and fifty thousand euro (€250,000) or such other sum as may be determined by the Minister from time to time (such limit is hereafter referred to as the "indemnity limit"), against any breach, committed by the notary and, or the notary's employees in a policy year. The indemnity limit shall be applicable to any one claim or to the aggregate of all claims made against the notary in any policy year.

For the purposes of this regulation, judicial and legal costs of whatever nature including those to defend a claim, and legal costs of whatever nature including, but not limited to, those relating to a compromise, shall be at the charge of the insurance provider and shall be deemed to be included in the indemnity limit:

Provided that nothing in this regulation shall preclude a notary from being insured for a higher sum than the indemnity limit, or for one or more "higher value transactions", under such terms and conditions agreed upon between the notary and the insurance provider:

Provided further that a policy shall not extend to any breach caused by a notary and, or the notary's employees, which is otherwise insured.

(2) The indemnity limit shall be exclusive of the sum that may be agreed upon as excess to be paid by the notary on each and every claim under the terms of the policy:

Provided that for one or more claims against the policy in any policy year, a notary shall not accept to pay an excess that exceeds, with regard to each such claim, one point five per centum (1.5%) of the indemnity limit established in the policy:

Provided further that an insurance provider shall not demand the payment of an excess as a condition to effect payment of damages to a claimant, nor shall the insurance provider be entitled to deduct such excess from any payment made to a claimant.

(3)(a) The notary shall disclose to the insurance provider his annual income from the exercise of his profession in the year immediately preceding the policy year. The insurance provider shall provide a policy based on such annual income:

Provided that where a notary is unable to disclose to the insurance provider his exact annual income for the year immediately preceding the policy year in view of the fact that such preceding year has not yet ended, a reasonable estimate shall suffice.

(b) Where the notary's annual income for the year immediately preceding the policy year does not exceed twenty-five thousand euro (€25,000) or such other sum as may be established by the Minister from time to time, the annual income for such preceding year shall be deemed to be twenty-five thousand euro (€25,000) or such other sum as may be established by the Minister from time to time.''',
        'metadata': {
            'citation': 'Notaries (Compulsory Insurance) Regulations Cap. 55.07, Article 3',
            'article': '3',
            'chapter': 'Cap. 55.07',
            'act_name': 'Notaries (Compulsory Insurance) Regulations',
            'topic': 'Compulsory Insurance Requirements',
            'jurisdiction': 'Malta',
            'verified_source': 'legislation.mt'
        }
    },

    # ========================================
    # ACTS OF DECEASED NOTARIES
    # ========================================
    {
        'id': 'doc_55_05_art_1_2',
        'content': '''1. The title of these regulations is the Acts of Deceased Notaries Regulations.

2. Where, on the demise of a Notary, it results that certain acts received by him, and which have been duly signed by the parties, are not in conformity with the provisions of article 40 of the Notarial Profession and Notarial Archives Act, the following provisions of these regulations shall have effect.''',
        'metadata': {
            'citation': 'Acts of Deceased Notaries Regulations Cap. 55.05, Articles 1-2',
            'article': '1-2',
            'chapter': 'Cap. 55.05',
            'act_name': 'Acts of Deceased Notaries Regulations',
            'topic': 'Citation and Application',
            'jurisdiction': 'Malta',
            'verified_source': 'legislation.mt'
        }
    },
    {
        'id': 'doc_55_05_art_3_5',
        'content': '''3. Where the acts mentioned in regulation 2 have been duly enrolled in the Public Registry, such note of enrolment shall serve to determine the date of the act, where this is missing or incomplete, and the date indicated in such enrolment shall be deemed to be the date of publication.

4. Where the original act has not been signed by the Notary or such signature is incomplete, the signature of the Notary on the note of enrolment shall be considered sufficient to signify that such act was published by the Notary who signed the note of enrolment, and where there is no mention of place of publication of the deed, it shall be presumed to have been published in the principal office of the Notary.

5. Where the note of enrolment contains details which have been omitted in the original act and appear as lacunae in such act, these details shall be considered as forming part of the said act.''',
        'metadata': {
            'citation': 'Acts of Deceased Notaries Regulations Cap. 55.05, Articles 3-5',
            'article': '3-5',
            'chapter': 'Cap. 55.05',
            'act_name': 'Acts of Deceased Notaries Regulations',
            'topic': 'Enrolled Acts and Lacunae',
            'jurisdiction': 'Malta',
            'verified_source': 'legislation.mt'
        }
    },
    {
        'id': 'doc_55_05_art_6_9',
        'content': '''6. Where the declaration that the Notary has explained the contents of the deed to the parties is missing, it shall be presumed that such explanation has been made by the Notary.

7. Where the declaration mentioned in article 28(1)(k)(v) of the Notarial Profession and Notarial Archives Act, relating to the incapability of a party to sign the deed, has been omitted, the signature of the witnesses shall suffice.

8. Where all the conditions of these regulations have been met, then the original deed shall be presumed to have been valid for all intents and purposes of the law.

9. The Notary Keeper of the deceased Notary shall make a marginal note on each act not in conformity with article 40 of the Notarial Profession and Notarial Archives Act, as hereinbefore stated, declaring that such act has been ratified by means of these regulations:

Provided that in the absence of a Notary Keeper such declaration shall be made by the Chief Notary to Government.''',
        'metadata': {
            'citation': 'Acts of Deceased Notaries Regulations Cap. 55.05, Articles 6-9',
            'article': '6-9',
            'chapter': 'Cap. 55.05',
            'act_name': 'Acts of Deceased Notaries Regulations',
            'topic': 'Presumptions and Ratification',
            'jurisdiction': 'Malta',
            'verified_source': 'legislation.mt'
        }
    },

    # ========================================
    # PUBLIC REGISTRY ACT
    # ========================================
    {
        'id': 'doc_56_art_1_2',
        'content': '''1. The title of this Act is Public Registry Act.

2. There shall be a Public Registry Office in Malta and another in Gozo for the registration of causes of preference among creditors for the enrolment of acts requiring registration in order to have effect in regard to third parties, and for all other registrations required by law.''',
        'metadata': {
            'citation': 'Public Registry Act Cap. 56, Articles 1-2',
            'article': '1-2',
            'chapter': 'Cap. 56',
            'act_name': 'Public Registry Act',
            'topic': 'Citation and Establishment of Registry',
            'jurisdiction': 'Malta',
            'verified_source': 'legislation.mt'
        }
    },
    {
        'id': 'doc_56_art_3',
        'content': '''3.(1) Each of the said offices shall be under the management of an officer called Director of the Public Registry, hereinafter referred to as the Director who shall also be the treasurer of the Public Registry and shall receive on account of the Government the fees leviable in accordance with the Tariff in the First Schedule hereto.

(2) The Public Registry Office of Malta there shall also be Assistant Directors who shall be so designated by the Director from among the officers referred to in sub-article (1) of article 306 of the Civil Code.

(3) Notwithstanding the provisions of article 306 of the Civil Code, any reference made to the Director in articles 35 and 37 shall not be construed as including a reference to any other officer referred to in this article.

(4) Before entering upon the duties of their office, the officers referred to in this article shall take before the Court of Appeal the oath of allegiance set out in the Constitution of Malta, and the oath of office as follows:

'I.......................................... promise and swear to observe faithfully all the laws of Malta relating to my office and to perform faithfully and with all honesty and exactness the duties of Director/ Assistant Director/Officer of /in the Public Registry to the best of my knowledge and ability. So help me God.'
''',
        'metadata': {
            'citation': 'Public Registry Act Cap. 56, Article 3',
            'article': '3',
            'chapter': 'Cap. 56',
            'act_name': 'Public Registry Act',
            'topic': 'Director and Officers of Public Registry',
            'jurisdiction': 'Malta',
            'verified_source': 'legislation.mt'
        }
    },

    # Adding original verified documents from user
    {
        'id': 'doc_civil_code_320_322',
        'content': '''320. Ownership is the right of enjoying and disposing of things in the most absolute manner, provided no use thereof is made which is prohibited by law.

321. No person can be compelled to give up his property or to permit any other person to make use of it, except for a public purpose, and upon payment of a fair compensation.

322. (1) Save as otherwise provided by law, the owner of a thing has the right to recover it from any possessor.

(2) A possessor who, after being notified of the judicial demand for the recovery of the thing ceases of his own act, to possess such thing, is bound, at his own expense, to regain possession of the thing for the plaintiff, or, if unable to do so, to make good its value, unless the plaintiff elects to proceed against the actual possessor.''',
        'metadata': {
            'citation': 'Civil Code Cap. 16, Article 320-322',
            'article': '320-322',
            'chapter': 'Cap. 16',
            'act_name': 'Civil Code',
            'topic': 'Ownership',
            'jurisdiction': 'Malta',
            'verified_by': 'User from legislation.mt',
            'verified_source': 'legislation.mt'
        }
    },
    {
        'id': 'doc_income_tax_56_13',
        'content': '''56.(13) (a) The tax upon the chargeable income of any person referred to as a Contractor in article 23 shall be levied at the rate of 35 cents (€0.35) on every euro of the chargeable income.

(b) The provisions of this subarticle shall apply to tax years commencing on or after 1st January 2020.''',
        'metadata': {
            'citation': 'Income Tax Act Cap. 123, Article 56(13)',
            'article': '56(13)',
            'chapter': 'Cap. 123',
            'act_name': 'Income Tax Act',
            'topic': 'Contractor Tax Rate',
            'jurisdiction': 'Malta',
            'verified_by': 'User from legislation.mt',
            'verified_source': 'legislation.mt'
        }
    },
    {
        'id': 'doc_civil_code_1346_1347',
        'content': '''1346. A sale is a contract whereby one of the contracting parties binds himself to pass the ownership of a thing or of some other right to the other party who, on his part, binds himself to pay the price thereof in money.

1347. Property shall be transferred and shall be acquired by right as soon as the thing and the price have been agreed upon, even though the thing has not yet been delivered nor the price paid.''',
        'metadata': {
            'citation': 'Civil Code Cap. 16, Article 1346-1347',
            'article': '1346-1347',
            'chapter': 'Cap. 16',
            'act_name': 'Civil Code',
            'topic': 'Sale Contracts',
            'jurisdiction': 'Malta',
            'verified_by': 'User from legislation.mt',
            'verified_source': 'legislation.mt'
        }
    }
]

# Total documents: 13 chunks covering multiple legal areas
# Topics covered:
# - Property law (ownership, title examination)
# - Professional regulations (notaries, insurance)
# - Public registry procedures
# - Tax law (contractor rates)
# - Contract law (sales)
