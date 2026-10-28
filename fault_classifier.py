def classify_fault(error):

    classifications = {

        "ENOENT": {
            "category": "File/Resource Error",
            "severity": "Medium",
            "action": "Check whether the required file or directory exists."
        },

        "EACCES": {
            "category": "Permission Error",
            "severity": "High",
            "action": "Check file permissions and access privileges."
        },

        "EBADF": {
            "category": "File Descriptor Error",
            "severity": "High",
            "action": "Check whether the file descriptor is valid and open."
        },

        "ENOMEM": {
            "category": "Memory Error",
            "severity": "High",
            "action": "Check memory allocation and available system memory."
        },

        "EFAULT": {
            "category": "Memory Address Error",
            "severity": "High",
            "action": "Check whether the memory address is valid."
        },

        "EINVAL": {
            "category": "Invalid Argument",
            "severity": "Medium",
            "action": "Check the arguments passed to the system call."
        },

        "EPERM": {
            "category": "Operation Not Permitted",
            "severity": "High",
            "action": "Check user privileges and system permissions."
        }

    }


    if error in classifications:

        return classifications[error]


    return {
        "category": "Unknown Error",
        "severity": "Medium",
        "action": "Investigate the system call and error condition."
    }