`git status` --> shows the status of the repo
`git log` --> shows the history of commits (--oneline better)
`git show HEAD` --> shows the last commit
`git show HEAD~1` --> shows the second last commit
`git diff HEAD~x HEAD~y` --> shows differences between x-last commit and y-last commit
`git diff` --> shows differences between working tree and Index
`git diff --cached` --> shows differences between last commit and Index (staged files)
`git diff HEAD` --> shows differences between last commit and working tree
`git remote -v` --> shows all linked remote repositories with URL
`git diff BRANCHNAME BRANCHNAME` --> compares differences between two branches

`git add FILE` --> stages given files (-A or . for all) --> only these files get commited afterwards
`git commit -m STRING` --> commits staged files to local repository (-a includes staging, -m STRING is needed)
`git commit` --amend -m STRING --> lets you rewrite the message of the last commit

`git push` --> push local repository to remote repository
`git pull` --> pull remote repository to workspace (local)
`git clone` --> makes a copy of the remote repository on your local computer (all in one --> git init, git remote add, git fetch, git checkout)

`git fetch` --> pull remote repository to local repository --> does not alter your workspace (existing parallel)

`git branch BRANCHNAME` --> creates branch
`git branch` --> lists you all branches of your local repo
`git branch --all` --> lists remote-tracking branches and local branches
`git checkout BRANCHNAME` --> switched between branches (changes the state of the working directory to the state of your local repo)
`git checkout -b BRANCHNAME COMMIT_ID` --> creates a new branch called BRANCHNAME on the specified commit (if no commit_id is given, than on HEAD) and switches to the branch
you can also reset your working directory or some special file with `git checkout HEAD PATH_TO_FILE` if you have not commited already and reset to a specified commit with `git checkout COMMIT_ID PATH_TO_FILE`
`git checkout COMMIT_ID` basically changes the HEAD to a certain commit
`git checkout PATH_TO_FILE` --> restores the file from the index to the working tree
--> you also can use **"." instead of PATH_TO_FILE/FILE_NAME** if you want to change **all files**

`git revert COMMIT_ID` undoes a certain commit and adds a new one (visible in commit history)
`git reset --soft COMMIT_ID` only deletes commit in commit history (local repo)
`git reset --mixed COMMIT_ID` also changes Index (only working directory stays the same)
`git reset --hard COMMIT_ID` changes all three trees (deletes completely)
instead of the **commit id** you also can write **"HEAD" or "@"** if you want to alter the last commit

`git merge` --> to merge remote and local repo together or to merge two branches (if both branches/repos are changed at the same place you can run into conflict)
`git mergetool` --> graphical tool to resolve merge conflicts
`git rebase` --> reapply the commits from one branch on top of the other