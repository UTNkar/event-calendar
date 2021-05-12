# Generated by Django 3.2.2 on 2021-05-12 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_sv', models.CharField(max_length=128, verbose_name='Swedish name')),
                ('name_en', models.CharField(max_length=128, verbose_name='English name')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_sv', models.CharField(max_length=256, verbose_name='Swedish event title')),
                ('title_en', models.CharField(max_length=256, verbose_name='English event title')),
                ('cover_photo', models.ImageField(upload_to='')),
                ('description_en', models.TextField(verbose_name='English event description')),
                ('description_sv', models.TextField(verbose_name='Swedish event description')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Last modified')),
                ('date_start', models.DateTimeField(help_text='Date and time when the event will start.', verbose_name='Event start date')),
                ('date_end', models.DateTimeField(blank=True, help_text='Leave empty if the event has no specific end time.', null=True, verbose_name='Event end date')),
                ('published', models.BooleanField(default=False)),
                ('membership_required', models.BooleanField(help_text='If the event requires a section or UTN membership.', verbose_name='Membership required')),
                ('contact', models.CharField(max_length=512)),
                ('location', models.CharField(blank=True, max_length=256)),
                ('price', models.CharField(blank=True, max_length=256)),
                ('link', models.URLField(blank=True, help_text='If your event has an important URL, such as a Zoom-link or Facebook page, enter it here.', verbose_name='URL')),
                ('categories', models.ManyToManyField(related_name='categories', to='event_calendar.Category', verbose_name='Event categories')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_en', models.CharField(max_length=128, verbose_name='English name')),
                ('name_sv', models.CharField(max_length=128, verbose_name='Swedish name')),
                ('description_en', models.TextField(blank=True, verbose_name='English description')),
                ('description_sv', models.TextField(blank=True, verbose_name='Swedish description')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Post contents')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Time of posting')),
                ('has_been_edited', models.BooleanField(default=False, verbose_name='Has been edited')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_calendar.group', verbose_name='Post creator')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='event_calendar.event', verbose_name='Related event')),
            ],
        ),
        migrations.CreateModel(
            name='EventCoHost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('invited', 'Invited'), ('accepted', 'Accepted')], default='invited', max_length=32)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_calendar.event')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_calendar.group')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='cohosts',
            field=models.ManyToManyField(related_name='cohosted_events', through='event_calendar.EventCoHost', to='event_calendar.Group', verbose_name='Event co-hosts'),
        ),
        migrations.AddField(
            model_name='event',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_calendar.group', verbose_name='Event host'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_calendar.group')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]