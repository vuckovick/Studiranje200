use studiranje200
go

CREATE TRIGGER ObrisanaOsoba
   ON  studiranje200_user200
   AFTER DELETE
AS 
BEGIN
	Declare @user_id int
	Declare @MyCursor cursor
	
	SET @MyCursor = CURSOR FOR
	select id
	from deleted

	OPEN @MyCursor
	FETCH NEXT FROM @MyCursor
	INTO @user_id

	WHILE @@FETCH_STATUS = 0
	BEGIN
		DELETE FROM studiranje200_connection
		WHERE follower_id = @user_id or followee_id = @user_id

		FETCH NEXT FROM @MyCursor
		INTO @user_id
	END
	CLOSE @MyCursor
	DEALLOCATE @MyCursor

END
GO
