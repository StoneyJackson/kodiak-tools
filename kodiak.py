from collections import namedtuple

PartsOfSubmissionFileName = namedtuple('PartsOfSubmissionFileName', 'submission_id first_name last_name date_time file_name')



def parse_submission_file_name(name):
    parts = name.split(' - ', maxsplit=3)
    first, last = parts[1].split(' ')
    return PartsOfSubmissionFileName(
        submission_id=parts[0],
        first_name=first,
        last_name=last,
        date_time=parts[2],
        file_name=parts[3]
        )
