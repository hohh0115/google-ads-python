# WAS HERE
USER_LIST_QUERY = """
    SELECT
        user_list.id,
        user_list.name,
        user_list.type,
        user_list.description,
        customer.id
    FROM user_list
"""
