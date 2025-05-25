import settings

if __name__ == "__main__":
    settings.set_book_id('7f39f8317fbdb1988ef4c628')  # 假设 book1 是一个有效的书籍ID

    today_word_list = settings.get_todays_word_list()
    print(today_word_list) # 输出今天的单词列表,类型为list[Word]

    first_word = today_word_list[0]
    settings.add_favourite(first_word.id)  # 将第一个单词添加到收藏夹

    settings.set_learned(first_word.id)  # 将第一个单词设置为已学(注意，如果错了也是已学习！)

    print(settings.get_favourite_list())  # 输出收藏夹列表,类型为list[Word]