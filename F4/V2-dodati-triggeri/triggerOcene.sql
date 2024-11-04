use studiranje200
go

CREATE TRIGGER Ocenivanje ON studiranje200_eventuser
   AFTER DELETE,UPDATE
AS 
BEGIN
	Declare @event_id int
	Declare @org_id int
	Declare @place_id int
	Declare @ratingNov int	
	Declare @ratingStar int

	Declare @NovaOcena cursor
	Declare @PromenjenaOcena cursor
	Declare @ObrisanaOcena cursor
	
	SET @NovaOcena = CURSOR FOR
	select i.event_id, i.rating
	from deleted d, inserted i 
	where d.event_id = i.event_id and i.status = N'attended' and d.status != N'attended'

	SET @PromenjenaOcena = CURSOR FOR
	select i.event_id, i.rating, d.rating
	from deleted d, inserted i 
	where d.event_id = i.event_id and i.status = N'attended' and d.status = N'attended'
	
	SET @ObrisanaOcena = CURSOR FOR
	select d.event_id, d.rating
	from deleted d, inserted i 
	where d.event_id not in ( select event_id from inserted )

	OPEN @NovaOcena
	FETCH NEXT FROM @NovaOcena
	INTO @event_id, @ratingNov

	WHILE @@FETCH_STATUS = 0
	BEGIN
		SELECT @place_id = place_id, @org_id = org_id
		FROM studiranje200_event 
		WHERE event_id = @event_id

		UPDATE studiranje200_event 
		SET total_rating = total_rating + @ratingNov, count_rating = count_rating + 1
		WHERE event_id = @event_id

		UPDATE studiranje200_organization
		SET total_rating = total_rating + @ratingNov, count_rating = count_rating + 1
		WHERE org_id = @org_id

		UPDATE studiranje200_place
		SET total_rating = total_rating + @ratingNov, count_rating = count_rating + 1
		WHERE place_id = @place_id

		FETCH NEXT FROM @NovaOcena
		INTO @event_id, @ratingNov
	END
	CLOSE @NovaOcena
	DEALLOCATE @NovaOcena

	OPEN @PromenjenaOcena
	FETCH NEXT FROM @PromenjenaOcena
	INTO @event_id, @ratingNov, @ratingStar

	WHILE @@FETCH_STATUS = 0
	BEGIN
		SELECT @place_id = place_id, @org_id = org_id
		FROM studiranje200_event 
		WHERE event_id = @event_id

		UPDATE studiranje200_event 
		SET total_rating = total_rating + @ratingNov - @ratingStar
		WHERE event_id = @event_id

		UPDATE studiranje200_organization
		SET total_rating = total_rating + @ratingNov - @ratingStar
		WHERE org_id = @org_id

		UPDATE studiranje200_place
		SET total_rating = total_rating + @ratingNov - @ratingStar
		WHERE place_id = @place_id

		FETCH NEXT FROM @PromenjenaOcena
		INTO @event_id, @ratingNov
	END
	CLOSE @PromenjenaOcena
	DEALLOCATE @PromenjenaOcena

	OPEN @ObrisanaOcena
	FETCH NEXT FROM @ObrisanaOcena
	INTO @event_id, @ratingNov

	WHILE @@FETCH_STATUS = 0
	BEGIN
		SELECT @place_id = place_id, @org_id = org_id
		FROM studiranje200_event 
		WHERE event_id = @event_id

		UPDATE studiranje200_event
		SET total_rating = total_rating - @ratingNov, count_rating = count_rating - 1
		WHERE event_id = @event_id

		UPDATE studiranje200_organization
		SET total_rating = total_rating - @ratingNov, count_rating = count_rating - 1
		WHERE org_id = @org_id

		UPDATE studiranje200_place
		SET total_rating = total_rating - @ratingNov, count_rating = count_rating - 1
		WHERE place_id = @place_id

		FETCH NEXT FROM @ObrisanaOcena
		INTO @event_id, @ratingNov
	END
	CLOSE @ObrisanaOcena
	DEALLOCATE @ObrisanaOcena
END
GO
