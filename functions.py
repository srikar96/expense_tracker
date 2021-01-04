import datetime as dt

def get_date_info(category, date):
    stamp = dt.datetime.today()
    year = stamp.year
    month = stamp.month
    day = stamp.day
    weekday = 1 if stamp.weekday() == 6 else (stamp.weekday()+2)

    general_dict = {'this year': 0, 'last year': 0, 'this month': 1, 'last month': 1, 'this week': 2, 'last week': 2, 'yesterday': 3, 'today': 3}
    month_dict = {'jan': 1, 'january': 1, 'feb': 2, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8, 'september': 9,
    'october': 10, 'november': 11, 'december': 12}
    day_dict = {'sunday': 1, 'monday': 2, 'tuesday': 3, 'wednesday': 4, 'thursday': 5, 'friday': 6, 'saturday': 7}

    # Complete Query with all parameters (pymongo)
    # cur = col1.aggregate([{'$project': {'_id':0, 'amount':1, 'year': {'$year': "$timestamp"}, 'month': {'$month': "$timestamp"}, 'day': { '$dayOfYear': "$timestamp" }, 'dayOfWeek': {'$dayOfWeek': "$timestamp"},
    # 'week': {'$week': "$timestamp"}}}, {'$match': {'category': xxx, 'year': 2019, 'month': 5, 'day': 45, 'dayOfWeek': 5, 'week':37}}])
    # Complete Query with all parameters (mongo)
#     db.expenses.aggregate(
#    [
#      {
#        $project:
#          {
#            year: { $year: "$timestamp" },
#
#            month: { $month: "$timestamp" },
#
#            day: { $dayOfMonth: "$timestamp" },
#            hour: { $hour: "$timestamp" },
#            minutes: { $minute: "$timestamp" },
#            seconds: { $second: "$timestamp" },
#            milliseconds: { $millisecond: "$timestamp" },
#            dayOfYear: { $dayOfYear: "$timestamp" },
#            dayOfWeek: { $dayOfWeek: "$timestamp" },
#            week: { $week: "$timestamp" }
#          }
#      }
#    ]
# )
    project = {'_id':0, 'amount':1}
    match = {}

    if date == 'this year':
        print('this year')
        project['year'] = {'$year': "$timestamp"}
        match['year'] = year
    elif date == 'last year':
        print('last year')
        project['year'] = {'$year': "$timestamp"}
        match['year'] = year-1
    elif date == 'this month':
        print('this month')
        project['year'] = {'$year': "$timestamp"}
        match['year'] = year
        project['month'] = {'$month': "$timestamp"}
        match['month'] = month
    elif date == 'last month':
        print('last month')
        project['year'] = {'$year': "$timestamp"}
        match['year'] = year
        project['month'] = {'$month': "$timestamp"}
        match['month'] = month-1
    elif date == 'this week':
        print('this week')
        project['year'] = {'$year': "$timestamp"}
        match['year'] = year
        project['week'] = {'$week': "$timestamp"}
        match['week'] = int(stamp.strftime('%V'))-1
    elif date == 'last week':
        print('last week')
        project['year'] = {'$year': "$timestamp"}
        match['year'] = year
        project['week'] = {'$week': "$timestamp"}
        match['week'] = int(stamp.strftime('%V'))-2
    elif date == 'today':
        print('today')
        project['year'] = {'$year': "$timestamp"}
        match['year'] = year
        project['month'] = {'$month': "$timestamp"}
        match['month'] = month
        project['day'] = {'$dayOfYear': "$timestamp"}
        match['day'] = int(stamp.strftime('%-j'))
    elif date == 'yesterday':
        print('yesterday')
        project['year'] = {'$year': "$timestamp"}
        match['year'] = year
        project['month'] = {'$month': "$timestamp"}
        match['month'] = month
        project['day'] = {'$dayOfYear': "$timestamp"}
        match['day'] = int(stamp.strftime('%-j'))-1
    elif date in month_dict:
        print('JAN FEB MAR')
        project['year'] = {'$year': "$timestamp"}
        match['year'] = year
        project['month'] = {'$month': "$timestamp"}
        match['month'] = month_dict[date]
    elif date in day_dict: #FIXME
        print('MON TUE WED')
        project['year'] = {'$year': "$timestamp"}
        match['year'] = year
        if day_dict[date] > weekday:
            print('greater')
            project['week'] = {'$week': "$timestamp"}
            match['week'] = int(stamp.strftime('%V'))-1
            project['dayOfWeek'] = {'$dayOfWeek': "$timestamp"}
            match['dayOfWeek'] = weekday
        else:
            print('lesser')
            project['week'] = {'$week': "$timestamp"}
            match['week'] = int(stamp.strftime('%V'))
            project['dayOfWeek'] = {'$dayOfWeek': "$timestamp"}
            match['dayOfWeek'] = weekday

    query = [{'$project': project}, {'$match': match}]

    if category:
        query[0]['$project']['category'] = 1
        query[1]['$match']['category'] = category

    return query
